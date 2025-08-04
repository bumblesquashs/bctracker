
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.trip import Trip

@dataclass(slots=True)
class TripRepository:
    
    database: Database
    
    def create(self, context: Context, row: dict):
        '''Inserts a new trip into the database'''
        self.database.insert(
            table='trip',
            values={
                'agency_id': context.agency_id,
                'system_id': context.system_id,
                'trip_id': row['trip_id'],
                'route_id': row['route_id'],
                'service_id': row['service_id'],
                'block_id': row['block_id'],
                'direction_id': int(row['direction_id']),
                'shape_id': row['shape_id'],
                'headsign': row['trip_headsign']
            }
        )
    
    def find(self, context: Context, trip_id: str) -> Trip | None:
        '''Returns the trip with the given context and trip ID'''
        trips = self.database.select(
            table='trip',
            columns=[
                'agency_id',
                'system_id',
                'trip_id',
                'route_id',
                'service_id',
                'block_id',
                'direction_id',
                'shape_id',
                'headsign'
            ],
            filters={
                'agency_id': context.agency_id,
                'system_id': context.system_id,
                'trip_id': trip_id
            },
            limit=1,
            initializer=Trip.from_db
        )
        try:
            return trips[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context, route_id: str | None = None, block_id: str | None = None, limit: int | None = None) -> list[Trip]:
        '''Returns all trips that match the given context, route, and block'''
        return self.database.select(
            table='trip',
            columns=[
                'agency_id',
                'system_id',
                'trip_id',
                'route_id',
                'service_id',
                'block_id',
                'direction_id',
                'shape_id',
                'headsign'
            ],
            filters={
                'agency_id': context.agency_id,
                'system_id': context.system_id,
                'route_id': route_id,
                'block_id': block_id
            },
            limit=limit,
            initializer=Trip.from_db
        )
    
    def delete_all(self, context: Context):
        '''Deletes all trips for the given context from the database'''
        self.database.delete(
            table='trip',
            filters={
                'agency_id': context.agency_id,
                'system_id': context.system_id
            }
        )
