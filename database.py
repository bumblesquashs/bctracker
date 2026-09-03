
import sqlite3
import shutil
from dataclasses import dataclass, field

from models.row import Row

@dataclass(slots=True)
class Database:
    
    name: str = 'bctracker'
    connection: sqlite3.Connection | None = field(default=None, init=False)
    
    def connect(self, foreign_keys=True, script_file='startup'):
        '''Opens a connection to the database and runs setup scripts'''
        if self.connection:
            return
        self.connection = sqlite3.connect(f'data/{self.name}.db', check_same_thread=False)
        if foreign_keys:
            self.connection.execute('PRAGMA foreign_keys = 1')
        else:
            self.connection.execute('PRAGMA foreign_keys = 0')
        self.connection.execute('PRAGMA case_sensitive_like = 0')
        
        if script_file:
            with open(f'sql/{script_file}.sql', 'r') as file:
                script = file.read()
            self.connection.cursor().executescript(script)
        
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
                if key == 'AND' or key == 'OR':
                    nested_expression, nested_args = self.build_where(value, key)
                    expressions.append(f'({nested_expression})')
                    args += nested_args
                elif type(value) is list:
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
