import sqlite3

connection = None

def connect():
    global connection
    connection = sqlite3.connect('data/bctracker.db', check_same_thread=False)
    connection.execute('PRAGMA foreign_keys = 1')

def disconnect():
    global connection
    connection.close()
    connection = None

def backup():
    backup = sqlite3.connect('archives/bctracker.db', check_same_thread=False)
    connection.backup(backup)
    backup.close()

def commit():
    connection.commit()

def execute(sql, args=None):
    args = [] if args is None else args
    
    if type(args) is list:
        args = tuple(args)
    if len(args) == 0:
        return connection.cursor().execute(sql)
    else:
        return connection.cursor().execute(sql, args)

def select(table, columns, distinct=False, ctes=None, joins=None, filters=None, operation='AND', group_by=None, order_by=None, limit=None, page=None, custom_args=None):
    custom_args = [] if custom_args is None else custom_args
    sql, args = build_select(table, columns, distinct, ctes, joins, filters, operation, group_by, order_by, limit, page)
    
    result = execute(sql, custom_args + args)
    if type(columns) is list:
        return [dict(zip(columns, r)) for r in result]
    elif type(columns) is dict:
        return [dict(zip(columns.values(), r)) for r in result]
    return result

def insert(table, values):
    if type(values) is dict:
        columns = values.keys()
        values = list(values.values())
        columns_string = ', '.join(columns)
        values_string = ', '.join(['?'] * len(values))
        sql = f'INSERT INTO {table} ({columns_string}) VALUES ({values_string})'
    else:
        if type(values) is not list:
            values = [values]
        values_string = ', '.join(['?'] * len(values))
        sql = f'INSERT INTO {table} VALUES ({values_string})'
    return execute(sql, values).lastrowid

def update(table, values, filters=None, operation='AND'):
    columns = values.keys()
    values = list(values.values())
    columns_string = ', '.join([c + ' = ?' for c in columns])
    
    where, args = build_where(filters, operation)
    if where is None:
        return execute(f'UPDATE {table} SET {columns_string}', values)
    return execute(f'UPDATE {table} SET {columns_string} WHERE {where}', values + args)

def delete(table, filters=None, operation='AND'):
    where, args = build_where(filters, operation)
    if where is None:
        return execute(f'DELETE FROM {table}')
    return execute(f'DELETE FROM {table} WHERE {where}', args)

def build_select(table, columns, distinct=False, ctes=None, joins=None, filters=None, operation='AND', group_by=None, order_by=None, limit=None, page=None, custom_args=None):
    custom_args = [] if custom_args is None else custom_args
    sql = []
    
    for cte in build_ctes(ctes):
        sql.append('WITH ' + cte)
    
    sql.append('SELECT')
    
    if distinct:
        sql.append('DISTINCT')
    
    if type(columns) is str:
        sql.append(columns)
    elif type(columns) is list:
        sql.append(', '.join(columns))
    elif type(columns) is dict:
        sql.append(', '.join([f'{k} AS {v}' for (k, v) in columns.items()]))
    else:
        sql.append('*')
    
    sql.append('FROM ' + table)
    
    for join in build_joins(joins):
        sql.append('JOIN ' + join)
    
    where, args = build_where(filters, operation)
    if where is not None:
        sql.append('WHERE ' + where)
    
    if type(group_by) is str:
        sql.append('GROUP BY ' + group_by)
    elif type(group_by) is list:
        sql.append('GROUP BY ' + ', '.join(group_by))
    
    if type(order_by) is str:
        sql.append('ORDER BY ' + order_by)
    elif type(order_by) is list:
        sql.append('ORDER BY ' + ', '.join(order_by))
    elif type(order_by) is dict:
        sql.append('ORDER BY ' + ', '.join([f'{k} {v}' for (k, v) in order_by.items()]))
    
    if type(limit) is int:
        sql.append(f'LIMIT {limit}')
        if type(page) is int:
            offset = limit * page
            sql.append(f'OFFSET {offset}')
    
    return ' '.join(sql), custom_args + args

def build_ctes(ctes):
    if type(ctes) is str:
        return [ctes]
    if type(ctes) is list:
        return ctes
    if type(ctes) is dict:
        return [f'{k} AS ({v})' for (k, v) in ctes.items()]
    return []

def build_joins(joins):
    if type(joins) is str:
        return [joins]
    elif type(joins) is list:
        return joins
    elif type(joins) is dict:
        results = []
        for key in joins.keys():
            join = [key]
            filters = joins[key]
            if type(filters) is str:
                join.append('ON ' + filters)
            elif type(filters) is list:
                join.append('ON ' + ' AND '.join(filters))
            elif type(filters) is dict:
                join.append('ON ' + ' AND '.join([f'{k} = {v}' for (k, v) in filters.items()]))
            results.append(' '.join(join))
        return results
    return []

def build_where(filters, operation):
    if type(filters) is str:
        return filters, []
    elif type(filters) is list:
        if len(filters) > 0:
            return f' {operation} '.join(filters), []
    elif type(filters) is dict:
        expressions = []
        args = []
        for key in filters.keys():
            value = filters[key]
            if value is None:
                continue
            if type(value) is list:
                args += value
                args_string = ', '.join(['?'] * len(value))
                expressions.append(f'{key} IN ({args_string})')
            elif type(value) is dict:
                for (k, v) in value.items():
                    if v is not None:
                        args.append(v)
                        expressions.append(f'{key} {k} ?')
            else:
                args.append(value)
                expressions.append(f'{key} = ?')
        if len(expressions) > 0:
            return f' {operation} '.join(expressions), args
    return None, []
