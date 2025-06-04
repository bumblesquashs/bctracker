
from dataclasses import dataclass

from database import Database

from models.area import Area
from models.context import Context
from models.stop import Stop

@dataclass(slots=True)
class StopRepository:
    
    database: Database
    
    def create(self, context: Context, row):
        '''Inserts a new stop into the database'''
        stop_id = row['stop_id']
        if 'stop_code' in row:
            number = row['stop_code']
            if not number:
                number = stop_id
        else:
            number = stop_id
        self.database.insert('stop', {
            'system_id': context.system_id,
            'stop_id': stop_id,
            'number': number,
            'name': row['stop_name'],
            'lat': float(row['stop_lat']),
            'lon': float(row['stop_lon'])
        })
    
    def find(self, context: Context, stop_id=None, number=None) -> Stop | None:
        '''Returns the stop with the given context and stop ID'''
        stops = self.database.select('stop',
            columns={
                'stop.system_id': 'system_id',
                'stop.stop_id': 'id',
                'stop.number': 'number',
                'stop.name': 'name',
                'stop.lat': 'lat',
                'stop.lon': 'lon'
            },
            filters={
                'stop.system_id': context.system_id,
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
    
    def find_all(self, context: Context, number=None, limit=None, lat=None, lon=None, size=0.01) -> list[Stop]:
        '''Returns all stops that match the given context'''
        filters = {
            'stop.system_id': context.system_id,
            'stop.number': number
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
                'stop.system_id': 'system_id',
                'stop.stop_id': 'id',
                'stop.number': 'number',
                'stop.name': 'name',
                'stop.lat': 'lat',
                'stop.lon': 'lon'
            },
            filters=filters,
            limit=limit,
            initializer=Stop.from_db
        )
    
    def find_all_ids(self, context: Context) -> list[str]:
        return self.database.select(
            table='stop',
            columns={
                'stop_id': 'id'
            },
            filters={
                'system_id': context.system_id
            },
            initializer=lambda r: r['id']
        )
    
    def find_area(self, context: Context) -> Area | None:
        '''Returns the area of all stops for the given context'''
        areas = self.database.select(
            table='stop',
            columns={
                'MIN(stop.lat)': 'min_lat',
                'MAX(stop.lat)': 'max_lat',
                'MIN(stop.lon)': 'min_lon',
                'MAX(stop.lon)': 'max_lon'
            },
            filters={
                'stop.system_id': context.system_id,
                'stop.lat': {
                    '!=': 0
                },
                'stop.lon': {
                    '!=': 0
                }
            },
            initializer=Area.from_db
        )
        try:
            return areas[0]
        except IndexError:
            return None
    
    def count(self) -> dict[str, int]:
        rows = self.database.select(
            table='stop',
            columns={
                'system_id': 'system_id',
                'COUNT(stop_id)': 'count'
            },
            group_by='system_id'
        )
        return { r['system_id']: r['count'] for r in rows }
    
    def delete_all(self, context: Context):
        '''Deletes all stops for the given context from the database'''
        self.database.delete('stop', {
            'system_id': context.system_id
        })
