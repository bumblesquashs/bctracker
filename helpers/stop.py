
from models.stop import Stop

import database

class StopService:
    
    def create(self, system, row):
        '''Inserts a new stop into the database'''
        system_id = getattr(system, 'id', system)
        database.default.insert('stop', {
            'system_id': system_id,
            'stop_id': row['stop_id'],
            'number': row['stop_code'],
            'name': row['stop_name'],
            'lat': float(row['stop_lat']),
            'lon': float(row['stop_lon'])
        })
    
    def find(self, system, stop_id=None, number=None):
        '''Returns the stop with the given system and stop ID'''
        system_id = getattr(system, 'id', system)
        stops = database.default.select('stop',
            columns={
                'stop.system_id': 'stop_system_id',
                'stop.stop_id': 'stop_id',
                'stop.number': 'stop_number',
                'stop.name': 'stop_name',
                'stop.lat': 'stop_lat',
                'stop.lon': 'stop_lon'
            },
            filters={
                'stop.system_id': system_id,
                'stop.stop_id': stop_id,
                'stop.number': number
            },
            limit=1,
            initializer=Stop.from_db
        )
        try:
            return stops[0]
        except IndexError:
            return None
    
    def find_all(self, system, limit=None):
        '''Returns all stops that match the given system'''
        system_id = getattr(system, 'id', system)
        return database.default.select('stop',
            columns={
                'stop.system_id': 'stop_system_id',
                'stop.stop_id': 'stop_id',
                'stop.number': 'stop_number',
                'stop.name': 'stop_name',
                'stop.lat': 'stop_lat',
                'stop.lon': 'stop_lon'
            },
            filters={
                'stop.system_id': system_id
            },
            limit=limit,
            initializer=Stop.from_db
        )
    
    def delete_all(self, system):
        '''Deletes all stops for the given system from the database'''
        system_id = getattr(system, 'id', system)
        database.default.delete('stop', {
            'system_id': system_id
        })

default = StopService()
