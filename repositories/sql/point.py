
from database import Database

from models.area import Area
from models.point import Point

from repositories import PointRepository

class SQLPointRepository(PointRepository):
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database: Database):
        self.database = database
    
    def create(self, system, row):
        '''Inserts a new point into the database'''
        system_id = getattr(system, 'id', system)
        self.database.insert('point', {
            'system_id': system_id,
            'shape_id': row['shape_id'],
            'sequence': int(row['shape_pt_sequence']),
            'lat': float(row['shape_pt_lat']),
            'lon': float(row['shape_pt_lon'])
        })
    
    def find_all(self, system, shape=None):
        '''Returns all points that match the given system and shape'''
        system_id = getattr(system, 'id', system)
        shape_id = getattr(shape, 'id', shape)
        return self.database.select('point',
            columns={
                'point.system_id': 'point_system_id',
                'point.shape_id': 'point_shape_id',
                'point.sequence': 'point_sequence',
                'point.lat': 'point_lat',
                'point.lon': 'point_lon'
            },
            filters={
                'point.system_id': system_id,
                'point.shape_id': shape_id
            },
            order_by='point.sequence ASC',
            initializer=Point.from_db
        )
    
    def find_area(self, system):
        system_id = getattr(system, 'id', system)
        areas = self.database.select(
            table='point',
            columns={
                'MIN(point.lat)': 'min_lat',
                'MAX(point.lat)': 'max_lat',
                'MIN(point.lon)': 'min_lon',
                'MAX(point.lon)': 'max_lon'
            },
            filters={
                'point.system_id': system_id
            },
            initializer=Area.from_db
        )
        try:
            return areas[0]
        except IndexError:
            return None
    
    def delete_all(self, system):
        '''Deletes all points for the given system from the database'''
        system_id = getattr(system, 'id', system)
        self.database.delete('point', {
            'point.system_id': system_id
        })
