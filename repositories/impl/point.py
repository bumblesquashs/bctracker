
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.point import Point

@dataclass(slots=True)
class PointRepository:
    
    database: Database
    
    def create(self, context: Context, row: dict):
        '''Inserts a new point into the database'''
        self.database.insert(
            table='point',
            values={
                # 'agency_id': context.agency_id,
                'system_id': context.system_id,
                'shape_id': row['shape_id'],
                'sequence': int(row['shape_pt_sequence']),
                'lat': float(row['shape_pt_lat']),
                'lon': float(row['shape_pt_lon'])
            }
        )
    
    def find_all(self, context: Context, shape_id: str) -> list[Point]:
        '''Returns all points that match the given context and shape'''
        return self.database.select(
            table='point',
            columns=[
                # 'agency_id',
                'system_id',
                'shape_id',
                'sequence',
                'lat',
                'lon'
            ],
            filters={
                # 'agency_id': context.agency_id,
                'system_id': context.system_id,
                'shape_id': shape_id
            },
            order_by='point.sequence ASC',
            initializer=Point.from_db
        )
    
    def delete_all(self, context: Context):
        '''Deletes all points for the given context from the database'''
        self.database.delete(
            table='point',
            filters={
                # 'agency_id': context.agency_id,
                'system_id': context.system_id
            }
        )
