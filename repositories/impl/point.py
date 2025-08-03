
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.point import Point

@dataclass(slots=True)
class PointRepository:
    
    database: Database
    
    def create(self, context: Context, row):
        '''Inserts a new point into the database'''
        self.database.insert(
            table='point',
            values={
                'system_id': context.system_id,
                'shape_id': row['shape_id'],
                'sequence': int(row['shape_pt_sequence']),
                'lat': float(row['shape_pt_lat']),
                'lon': float(row['shape_pt_lon'])
            }
        )
    
    def find_all(self, context: Context, shape=None) -> list[Point]:
        '''Returns all points that match the given context and shape'''
        shape_id = getattr(shape, 'id', shape)
        return self.database.select(
            table='point',
            columns={
                'point.system_id': 'system_id',
                'point.shape_id': 'shape_id',
                'point.sequence': 'sequence',
                'point.lat': 'lat',
                'point.lon': 'lon'
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
        self.database.delete(
            table='point',
            filters={
                'point.system_id': context.system_id
            }
        )
