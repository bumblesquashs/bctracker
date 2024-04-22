
from di import di

from models.stop import Stop

from database import Database

class StopService:
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, **kwargs):
        self.database = kwargs.get('database') or di[Database]
    
    def create(self, system, row):
        '''Inserts a new stop into the database'''
        system_id = getattr(system, 'id', system)
        self.database.insert('stop', {
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
        stops = self.database.select('stop',
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
        return self.database.select('stop',
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
        self.database.delete('stop', {
            'system_id': system_id
        })
