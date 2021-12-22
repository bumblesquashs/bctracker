import sqlite3

connection = None

def connect():
    global connection
    connection = sqlite3.connect('data/bctracker.db', check_same_thread=False)

def disconnect():
    global connection
    connection.close()
    connection = None

def commit():
    connection.commit()

def execute(sql, args=None):
    if type(args) is list:
        args = tuple(args)
    if args is None:
        return connection.cursor().execute(sql)
    else:
        return connection.cursor().execute(sql, args)

def select(table, columns='*', filters=None, order_by=None, limit=None, args=None):
    if type(columns) is not list:
        columns = [columns]
    columns_string = ', '.join(columns)
    sql = f'SELECT {columns_string} FROM {table}'
    if type(filters) is str:
        sql += f' WHERE {filters}'
    elif type(filters) is list:
        filters_string = ' AND '.join(filters)
        sql += f' WHERE {filters_string}'
    elif type(filters) is dict:
        keys = filters.keys()
        args = [filters[k] for k in keys]
        filters_string = ' AND '.join([f'{k} = ?' for k in keys])
        sql += f' WHERE {filters_string}'
    if order_by is not None:
        sql += f' ORDER BY {order_by}'
    if limit is not None:
        sql += f' LIMIT {int(limit)}'
    result = execute(sql, args)
    if columns == ['*']:
        return result
    return [dict(zip(columns, r)) for r in result]

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
    return execute(sql, values)

def update(table, values, filters=None, args=None):
    columns = values.keys()
    values = list(values.values())
    columns_string = ', '.join([c + ' = ?' for c in columns])
    sql = f'UPDATE {table} SET {columns_string}'
    if type(filters) is str:
        sql += f' WHERE {filters}'
    elif type(filters) is list:
        filters_string = ' AND '.join(filters)
        sql += f' WHERE {filters_string}'
    elif type(filters) is dict:
        keys = filters.keys()
        args = [filters[k] for k in keys]
        filters_string = ' AND '.join([f'{k} = ?' for k in keys])
        sql += f' WHERE {filters_string}'
    return execute(sql, values + args)

def backup():
    backup = sqlite3.connect('archives/bctracker.db', check_same_thread=False)
    connection.backup(backup)
    backup.close()
