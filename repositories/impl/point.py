
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.point import Point

@dataclass(slots=True)
class PointRepository:
    
    database: Database
    
    def create(self, download_id: int, context: Context, row: dict):
        '''Inserts a new point into the database'''
        self.database.insert(
            table='point',
            values={
                'download_id': download_id,
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
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'point.shape_id': 'shape_id',
                'point.sequence': 'sequence',
                'point.lat': 'lat',
                'point.lon': 'lon'
            },
            joins={
                'download': {
                    'download.download_id': 'point.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
                'point.shape_id': shape_id
            },
            order_by='point.sequence ASC',
            initializer=Point.from_db
        )
    
    def delete_all(self, context: Context):
        '''Deletes all points for the given context from the database'''
        download_ids = self.database.select(
            table='point',
            columns={
                'point.download_id': 'download_id'
            },
            distinct=True,
            joins={
                'download': {
                    'download.download_id': 'point.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id
            },
            initializer=lambda r: r['download_id']
        )
        if not download_ids:
            return
        if len(download_ids) == 1:
            download_ids = download_ids[0]
        self.database.delete(
            table='point',
            filters={
                'download_id': download_ids
            }
        )
