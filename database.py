
import sqlite3
import shutil
from dataclasses import dataclass, field

from models.row import Row

SQL_SCRIPTS = [
    '''
        CREATE TABLE IF NOT EXISTS allocation (
            allocation_id INTEGER PRIMARY KEY ASC,
            agency_id TEXT NOT NULL,
            vehicle_id TEXT NOT NULL,
            system_id TEXT,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            active INTEGER NOT NULL,
            last_lat REAL,
            last_lon REAL,
            last_stop_id TEXT,
            last_stop_number TEXT,
            last_stop_name TEXT,
            last_seen_timestamp REAL
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS record (
            record_id INTEGER PRIMARY KEY ASC,
            allocation_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            block_id TEXT,
            route_numbers TEXT,
            start_time TEXT,
            end_time TEXT,
            first_seen TEXT,
            last_seen TEXT,
            FOREIGN KEY (allocation_id) REFERENCES allocation (allocation_id)
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
        CREATE TABLE IF NOT EXISTS allocation_record (
            allocation_id INTEGER UNIQUE NOT NULL,
            first_record_id INTEGER,
            last_record_id INTEGER,
            FOREIGN KEY (allocation_id) REFERENCES allocation (allocation_id),
            FOREIGN KEY (first_record_id) REFERENCES record (record_id),
            FOREIGN KEY (last_record_id) REFERENCES record (record_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS transfer (
            transfer_id INTEGER PRIMARY KEY ASC,
            date TEXT NOT NULL,
            old_allocation_id INTEGER NOT NULL,
            new_allocation_id INTEGER NOT NULL,
            FOREIGN KEY (old_allocation_id) REFERENCES allocation (allocation_id),
            FOREIGN KEY (new_allocation_id) REFERENCES allocation (allocation_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS position (
            agency_id TEXT NOT NULL,
            vehicle_id TEXT NOT NULL,
            system_id TEXT,
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
            layover INTEGER,
            occupancy TEXT,
            timestamp REAL,
            PRIMARY KEY (agency_id, vehicle_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS assignment (
            block_id TEXT NOT NULL,
            allocation_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            PRIMARY KEY (block_id, allocation_id),
            FOREIGN KEY (allocation_id) REFERENCES allocation (allocation_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS route (
            agency_id TEXT NOT NULL,
            system_id TEXT,
            route_id TEXT NOT NULL,
            number TEXT NOT NULL,
            name TEXT NOT NULL,
            colour TEXT,
            text_colour TEXT,
            type TEXT,
            sort_order INTEGER,
            PRIMARY KEY (agency_id, system_id, route_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS stop (
            agency_id TEXT NOT NULL,
            system_id TEXT,
            stop_id TEXT NOT NULL,
            number TEXT NOT NULL,
            name TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            parent_id TEXT,
            type TEXT,
            PRIMARY KEY (agency_id, system_id, stop_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS trip (
            agency_id TEXT NOT NULL,
            system_id TEXT,
            trip_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            block_id TEXT,
            direction_id TEXT,
            shape_id INTEGER,
            headsign TEXT NOT NULL,
            PRIMARY KEY (agency_id, system_id, trip_id),
            FOREIGN KEY (agency_id, system_id, route_id) REFERENCES route (agency_id, system_id, route_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS departure (
            agency_id TEXT NOT NULL,
            system_id TEXT,
            trip_id TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            stop_id TEXT NOT NULL,
            time TEXT NOT NULL,
            pickup_type TEXT NOT NULL,
            dropoff_type TEXT NOT NULL,
            timepoint INTEGER NOT NULL,
            distance REAL,
            headsign TEXT,
            PRIMARY KEY (agency_id, system_id, trip_id, sequence),
            FOREIGN KEY (agency_id, system_id, trip_id) REFERENCES trip (agency_id, system_id, trip_id),
            FOREIGN KEY (agency_id, system_id, stop_id) REFERENCES stop (agency_id, system_id, stop_id)
        )
    ''',
    '''
        CREATE TABLE IF NOT EXISTS point (
            agency_id TEXT NOT NULL,
            system_id TEXT,
            shape_id TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            PRIMARY KEY (agency_id, system_id, shape_id, sequence)
        )
    ''',
    'CREATE INDEX IF NOT EXISTS allocation_agency_vehicle ON allocation (agency_id, vehicle_id)',
    'CREATE INDEX IF NOT EXISTS record_allocation ON record (allocation_id)',
    'CREATE INDEX IF NOT EXISTS trip_record_record_id ON trip_record (record_id)',
    'CREATE INDEX IF NOT EXISTS transfer_old_allocation ON transfer (old_allocation_id)',
    'CREATE INDEX IF NOT EXISTS transfer_new_allocation ON transfer (new_allocation_id)',
    'CREATE INDEX IF NOT EXISTS departure_trip_id ON departure (trip_id)',
    'CREATE INDEX IF NOT EXISTS departure_stop_id ON departure (stop_id)'
]

@dataclass(slots=True)
class Database:
    
    name: str = 'bctracker'
    connection: sqlite3.Connection | None = field(default=None, init=False)
    
    def connect(self, foreign_keys=True, run_scripts=True):
        '''Opens a connection to the database and runs setup scripts'''
        if self.connection:
            return
        self.connection = sqlite3.connect(f'data/{self.name}.db', check_same_thread=False)
        if foreign_keys:
            self.connection.execute('PRAGMA foreign_keys = 1')
        else:
            self.connection.execute('PRAGMA foreign_keys = 0')
        
        if run_scripts:
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
                return [initializer(Row(dict(zip(columns, r)))) for r in result]
            return [Row(dict(zip(columns, r))) for r in result]
        elif type(columns) is dict:
            if initializer:
                return [initializer(Row(dict(zip(columns.values(), r)))) for r in result]
            return [Row(dict(zip(columns.values(), r))) for r in result]
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
    
    def upsert(self, table: str, conflict_column: str, insert_values: dict | list, update_values: dict):
        sql = [f'INSERT INTO {table}']
        
        if type(insert_values) is dict:
            insert_columns = insert_values.keys()
            insert_values_list = list(insert_values.values())
            insert_columns_string = ', '.join(insert_columns)
            insert_values_string = ', '.join(['?'] * len(insert_values_list))
            sql.append(f'({insert_columns_string}) VALUES ({insert_values_string})')
        else:
            if type(insert_values) is list:
                insert_values_list = insert_values
            else:
                insert_values_list = [insert_values]
            insert_values_string = ', '.join(['?'] * len(insert_values_list))
            sql.append(f'VALUES ({insert_values_string})')
        
        sql.append(f'ON CONFLICT({conflict_column}) DO UPDATE SET')
        
        update_columns = update_values.keys()
        update_values_list = list(update_values.values())
        update_columns_string = ', '.join([c + ' = ?' for c in update_columns])
        sql.append(update_columns_string)
        
        return self.execute(' '.join(sql), insert_values_list + update_values_list)
    
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
                offset = limit * (page - 1)
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
            if filters:
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
            if expressions:
                return f' {operation} '.join(expressions), args
        return None, []
