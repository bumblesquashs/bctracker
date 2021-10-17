import sqlite3

connection = None

def connect():
    global connection
    connection = sqlite3.connect('data/bctracker.db', check_same_thread=False)

def disconnect():
    global connection
    connection.close()
    connection = None

def execute(sql, args=None):
    if type(args) is list:
        args = tuple(args)
    if args is None:
        result = connection.cursor().execute(sql)
    else:
        result = connection.cursor().execute(sql, args)
    connection.commit()
    return result

def select(table, columns='*', filters=None, limit=None, args=None):
    if type(columns) is not list:
        columns = [columns]
    columns_string = ', '.join(columns)
    sql = f'SELECT {columns_string} FROM {table}'
    if filters is not None:
        if type(filters) is not list:
            filters = [filters]
        filters_string = ' AND '.join(filters)
        sql += f' WHERE {filters_string}'
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
    if filters is not None:
        if type(filters) is not list:
            filters = [filters]
        filters_string = ' AND '.join(filters)
        sql += f' WHERE {filters_string}'
    return execute(sql, values + args)
