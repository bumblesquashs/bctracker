
import sqlite3
import shutil

from services import Database

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
        CREATE TABLE IF NOT EXISTS route (
            system_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            number TEXT NOT NULL,
            name TEXT NOT NULL,
            colour TEXT,
            text_colour TEXT,
            PRIMARY KEY (system_id, route_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS stop (
            system_id TEXT NOT NULL,
            stop_id TEXT NOT NULL,
            number TEXT NOT NULL,
            name TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            PRIMARY KEY (system_id, stop_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS trip (
            system_id TEXT NOT NULL,
            trip_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            block_id TEXT,
            direction_id TEXT,
            shape_id INTEGER,
            headsign TEXT NOT NULL,
            PRIMARY KEY (system_id, trip_id),
            FOREIGN KEY (system_id, route_id) REFERENCES route (system_id, route_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS departure (
            system_id TEXT NOT NULL,
            trip_id TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            stop_id TEXT NOT NULL,
            time TEXT NOT NULL,
            pickup_type TEXT NOT NULL,
            dropoff_type TEXT NOT NULL,
            timepoint INTEGER NOT NULL,
            distance REAL,
            PRIMARY KEY (system_id, trip_id, sequence),
            FOREIGN KEY (system_id, trip_id) REFERENCES trip (system_id, trip_id),
            FOREIGN KEY (system_id, stop_id) REFERENCES stop (system_id, stop_id)
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
    '''
        CREATE TABLE IF NOT EXISTS assignment (
            system_id TEXT NOT NULL,
            block_id TEXT NOT NULL,
            bus_number INTEGER NOT NULL,
            date TEXT NOT NULL,
            PRIMARY KEY (system_id, block_id)
        )
    ''',
    'CREATE INDEX IF NOT EXISTS record_bus_number ON record (bus_number)',
    'CREATE INDEX IF NOT EXISTS trip_record_record_id ON trip_record (record_id)',
    'CREATE INDEX IF NOT EXISTS transfer_bus_number ON transfer (bus_number)'
]

class DefaultDatabase(Database):
    
    __slots__ = (
        'name',
        'connection'
    )
    
    def __init__(self, name='bctracker'):
        self.name = name
        self.connection = None
    
    def connect(self, foreign_keys=True):
        '''Opens a connection to the database and runs setup scripts'''
        if self.connection:
            return
        self.connection = sqlite3.connect(f'data/{self.name}.db', check_same_thread=False)
        if foreign_keys:
            self.connection.execute('PRAGMA foreign_keys = 1')
        else:
            self.connection.execute('PRAGMA foreign_keys = 0')
        
        for sql in SQL_SCRIPTS:
            self.execute(sql)
        self.commit()
    
    def disconnect(self):
        '''Closes the connection to the database'''
        if not self.connection:
            return
        self.connection.close()
        self.connection = None
    
    def archive(self):
        '''Creates a duplicate database file in the archives folder'''
        shutil.copyfile(f'./data/{self.name}.db', f'./archives/{self.name}.db')
    
    def commit(self):
        '''Saves all changes made to the database'''
        if not self.connection:
            return
        self.connection.commit()
    
    def execute(self, sql, args=None):
        '''Runs a generic SQL script with the given arguments'''
        if not self.connection:
            return
        args = [] if args is None else args
        
        if type(args) is list:
            args = tuple(args)
        if args:
            return self.connection.cursor().execute(sql, args)
        return self.connection.cursor().execute(sql)
    
    def select(self, table, columns, distinct=False, ctes=None, join_type='', joins=None, filters=None, operation='AND', group_by=None, order_by=None, limit=None, page=None, custom_args=None, initializer=None):
        '''Executes a SELECT script and returns the selected rows'''
        custom_args = [] if custom_args is None else custom_args
        sql, args = self.build_select(table, columns, distinct, ctes, join_type, joins, filters, operation, group_by, order_by, limit, page)
        
        result = self.execute(sql, custom_args + args)
        if type(columns) is list:
            if initializer:
                return [initializer(dict(zip(columns, r))) for r in result]
            return [dict(zip(columns, r)) for r in result]
        elif type(columns) is dict:
            if initializer:
                return [initializer(dict(zip(columns.values(), r))) for r in result]
            return [dict(zip(columns.values(), r)) for r in result]
        return result
    
    def insert(self, table, values):
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
        return self.execute(sql, values).lastrowid
    
    def update(self, table, values, filters=None, operation='AND'):
        '''Executes an UPDATE script'''
        columns = values.keys()
        values = list(values.values())
        columns_string = ', '.join([c + ' = ?' for c in columns])
        
        where, args = self.build_where(filters, operation)
        if where:
            return self.execute(f'UPDATE {table} SET {columns_string} WHERE {where}', values + args)
        return self.execute(f'UPDATE {table} SET {columns_string}', values)
    
    def delete(self, table, filters=None, operation='AND'):
        '''Executes a DELETE script'''
        where, args = self.build_where(filters, operation)
        if where:
            return self.execute(f'DELETE FROM {table} WHERE {where}', args)
        return self.execute(f'DELETE FROM {table}')
    
    def build_select(self, table, columns, distinct=False, ctes=None, join_type='', joins=None, filters=None, operation='AND', group_by=None, order_by=None, limit=None, page=None, custom_args=None):
        '''Creates a SQL script for a SELECT query'''
        custom_args = [] if custom_args is None else custom_args
        sql = []
        
        for cte in self.build_ctes(ctes):
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
        
        for join in self.build_joins(joins):
            sql.append(join_type + ' JOIN ' + join)
        
        where, args = self.build_where(filters, operation)
        if where:
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
    
    def build_ctes(self, ctes):
        '''Creates a SQL script for common table expressions'''
        if type(ctes) is str:
            return [ctes]
        if type(ctes) is list:
            return ctes
        if type(ctes) is dict:
            return [f'{k} AS ({v})' for (k, v) in ctes.items()]
        return []
    
    def build_joins(self, joins):
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
    
    def build_where(self, filters, operation):
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
