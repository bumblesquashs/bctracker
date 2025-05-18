
from database import Database

from models.context import Context
from models.point import Point

class PointRepository:
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database: Database):
        self.database = database
    
    def create(self, context: Context, row):
        '''Inserts a new point into the database'''
        self.database.insert('point', {
            'system_id': context.system_id,
            'shape_id': row['shape_id'],
            'sequence': int(row['shape_pt_sequence']),
            'lat': float(row['shape_pt_lat']),
            'lon': float(row['shape_pt_lon'])
        })
    
    def find_all(self, context: Context, shape=None):
        '''Returns all points that match the given context and shape'''
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
                'point.system_id': context.system_id,
                'point.shape_id': shape_id
            },
            order_by='point.sequence ASC',
            initializer=Point.from_db
        )
    
    def delete_all(self, context: Context):
        '''Deletes all points for the given context from the database'''
        self.database.delete('point', {
            'point.system_id': context.system_id
        })
