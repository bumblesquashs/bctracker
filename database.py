import sqlite3

SQL_SCRIPTS = [
    '''
        CREATE TABLE IF NOT EXISTS record (
            record_id INTEGER PRIMARY KEY ASC,
            bus_number INTEGER NOT NULL,
            date TEXT NOT NULL,
            system_id TEXT NOT NULL,
            block_id TEXT NOT NULL,
            routes TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            first_seen TEXT,
            last_seen TEXT
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS trip_record (
            trip_record_id INTEGER PRIMARY KEY ASC,
            record_id INTEGER NOT NULL,
            trip_id TEXT NOT NULL,
            FOREIGN KEY (record_id) REFERENCES record (record_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS transfer (
            transfer_id INTEGER PRIMARY KEY ASC,
            bus_number INTEGER NOT NULL,
            date TEXT NOT NULL,
            old_system_id TEXT NOT NULL,
            new_system_id TEXT NOT NULL
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS overview (
            bus_number INTEGER PRIMARY KEY,
            first_seen_date TEXT NOT NULL,
            first_seen_system_id TEXT NOT NULL,
            first_record_id INTEGER,
            last_seen_date TEXT NOT NULL,
            last_seen_system_id TEXT NOT NULL,
            last_record_id INTEGER,
            FOREIGN KEY (first_record_id) REFERENCES record (record_id),
            FOREIGN KEY (last_record_id) REFERENCES record (record_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS position (
            system_id TEXT NOT NULL,
            bus_number INTEGER NOT NULL,
            trip_id TEXT,
            stop_id TEXT,
            block_id TEXT,
            route_id TEXT,
            sequence INTEGER,
            lat REAL,
            lon REAL,
            bearing REAL,
            speed INTEGER,
            adherence INTEGER,
            PRIMARY KEY (system_id, bus_number)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS point (
            system_id TEXT NOT NULL,
            shape_id TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            PRIMARY KEY (system_id, shape_id, sequence)
        )
    ''',
    'CREATE INDEX IF NOT EXISTS record_bus_number ON record (bus_number)',
    'CREATE INDEX IF NOT EXISTS trip_record_record_id ON trip_record (record_id)',
    'CREATE INDEX IF NOT EXISTS transfer_bus_number ON transfer (bus_number)'
]

connection = None

def connect(name='bctracker', foreign_keys=True):
    '''Opens a connection to the database and runs setup scripts'''
    global connection
    connection = sqlite3.connect(f'data/{name}.db', check_same_thread=False)
    if foreign_keys:
        connection.execute('PRAGMA foreign_keys = 1')
    else:
        connection.execute('PRAGMA foreign_keys = 0')
    
    for sql in SQL_SCRIPTS:
        execute(sql)
    commit()

def disconnect():
    '''Closes the connection to the database'''
    global connection
    if connection is None:
        return
    connection.close()
    connection = None

def backup():
    '''Copies all information from the main database to a backup database'''
    if connection is None:
        return
    backup = sqlite3.connect('archives/bctracker.db', check_same_thread=False)
    connection.backup(backup)
    backup.close()

def commit():
    '''Saves all changes made to the database'''
    if connection is None:
        return
    connection.commit()

def execute(sql, args=None):
    '''Runs a generic SQL script with the given arguments'''
    if connection is None:
        return
    args = [] if args is None else args
    
    if type(args) is list:
        args = tuple(args)
    if len(args) == 0:
        return connection.cursor().execute(sql)
    else:
        return connection.cursor().execute(sql, args)

def select(table, columns, distinct=False, ctes=None, join_type='', joins=None, filters=None, operation='AND', group_by=None, order_by=None, limit=None, page=None, custom_args=None):
    '''Executes a SELECT script and returns the selected rows'''
    custom_args = [] if custom_args is None else custom_args
    sql, args = build_select(table, columns, distinct, ctes, join_type, joins, filters, operation, group_by, order_by, limit, page)
    
    result = execute(sql, custom_args + args)
    if type(columns) is list:
        return [dict(zip(columns, r)) for r in result]
    elif type(columns) is dict:
        return [dict(zip(columns.values(), r)) for r in result]
    return result

def insert(table, values):
    '''Executes an INSERT script and returns the new row ID'''
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
    '''Executes an UPDATE script'''
    columns = values.keys()
    values = list(values.values())
    columns_string = ', '.join([c + ' = ?' for c in columns])
    
    where, args = build_where(filters, operation)
    if where is None:
        return execute(f'UPDATE {table} SET {columns_string}', values)
    return execute(f'UPDATE {table} SET {columns_string} WHERE {where}', values + args)

def delete(table, filters=None, operation='AND'):
    '''Executes a DELETE script'''
    where, args = build_where(filters, operation)
    if where is None:
        return execute(f'DELETE FROM {table}')
    return execute(f'DELETE FROM {table} WHERE {where}', args)

def build_select(table, columns, distinct=False, ctes=None, join_type='', joins=None, filters=None, operation='AND', group_by=None, order_by=None, limit=None, page=None, custom_args=None):
    '''Creates a SQL script for a SELECT query'''
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
        sql.append(join_type + ' JOIN ' + join)
    
    where, args = build_where(filters, operation)
    if where is not None:
        sql.append('WHERE ' + where)
    
    if type(group_by) is str:
        sql.append('GROUP BY ' + group_by)
    elif type(group_by) is list or type(group_by) is set:
        sql.append('GROUP BY ' + ', '.join(group_by))
    
    if type(order_by) is str:
        sql.append('ORDER BY ' + order_by)
    elif type(order_by) is list or type(order_by) is set:
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
    '''Creates a SQL script for common table expressions'''
    if type(ctes) is str:
        return [ctes]
    if type(ctes) is list:
        return ctes
    if type(ctes) is dict:
        return [f'{k} AS ({v})' for (k, v) in ctes.items()]
    return []

def build_joins(joins):
    '''Creates a SQL script for table joins'''
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
    '''Creates a SQL script for a WHERE filter'''
    if type(filters) is str:
        return filters, []
    elif type(filters) is list or type(filters) is set:
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
            elif type(value) is set:
                args += list(value)
                args_string = ', '.join(['?'] * len(value))
                expressions.append(f'{key} IN ({args_string})')
            elif type(value) is dict:
                for (k, v) in value.items():
                    if v is None:
                        if k == 'IS' or k == 'IS NOT':
                            expressions.append(f'{key} {k} NULL')
                    else:
                        args.append(v)
                        expressions.append(f'{key} {k} ?')
            else:
                args.append(value)
                expressions.append(f'{key} = ?')
        if len(expressions) > 0:
            return f' {operation} '.join(expressions), args
    return None, []
