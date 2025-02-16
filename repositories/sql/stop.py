
from database import Database

from models.area import Area
from models.stop import Stop

from repositories import StopRepository

class SQLStopRepository(StopRepository):
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database: Database):
        self.database = database
    
    def create(self, system, row):
        '''Inserts a new stop into the database'''
        system_id = getattr(system, 'id', system)
        stop_id = row['stop_id']
        number = row['stop_code']
        if not number:
            number = stop_id
        self.database.insert('stop', {
            'system_id': system_id,
            'stop_id': stop_id,
            'number': number,
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
    
    def find_all(self, system, limit=None, lat=None, lon=None, size=0.01):
        '''Returns all stops that match the given system'''
        system_id = getattr(system, 'id', system)
        filters = {
            'stop.system_id': system_id
        }
        if (lat is not None and lon is not None):
            filters['lat'] = {
                '>=': lat,
                '<=': lat + size
            }
            filters['lon'] = {
                '>=': lon,
                '<=': lon + size
            }
        return self.database.select('stop',
            columns={
                'stop.system_id': 'stop_system_id',
                'stop.stop_id': 'stop_id',
                'stop.number': 'stop_number',
                'stop.name': 'stop_name',
                'stop.lat': 'stop_lat',
                'stop.lon': 'stop_lon'
            },
            filters=filters,
            limit=limit,
            initializer=Stop.from_db
        )
    
    def find_area(self, system):
        system_id = getattr(system, 'id', system)
        areas = self.database.select(
            table='stop',
            columns={
                'MIN(stop.lat)': 'min_lat',
                'MAX(stop.lat)': 'max_lat',
                'MIN(stop.lon)': 'min_lon',
                'MAX(stop.lon)': 'max_lon'
            },
            filters={
                'stop.system_id': system_id
            },
            initializer=Area.from_db
        )
        try:
            return areas[0]
        except IndexError:
            return None
    
    def delete_all(self, system):
        '''Deletes all stops for the given system from the database'''
        system_id = getattr(system, 'id', system)
        self.database.delete('stop', {
            'system_id': system_id
        })
