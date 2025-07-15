
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.trip import Trip

@dataclass(slots=True)
class TripRepository:
    
    database: Database
    
    def create(self, context: Context, row):
        '''Inserts a new trip into the database'''
        trip_id = row['trip_id']
        block_id = row.get('block_id', trip_id)
        if 'direction_id' in row:
            direction_id = int(row['direction_id'])
        else:
            direction_id = 0
        self.database.insert('trip', {
            'system_id': context.system_id,
            'trip_id': trip_id,
            'route_id': row['route_id'],
            'service_id': row['service_id'],
            'block_id': block_id,
            'direction_id': direction_id,
            'shape_id': row['shape_id'],
            'headsign': row['trip_headsign']
        })
    
    def find(self, context: Context, trip_id) -> Trip | None:
        '''Returns the trip with the given context and trip ID'''
        trips = self.database.select('trip',
            columns={
                'trip.system_id': 'system_id',
                'trip.trip_id': 'id',
                'trip.route_id': 'route_id',
                'trip.service_id': 'service_id',
                'trip.block_id': 'block_id',
                'trip.direction_id': 'direction_id',
                'trip.shape_id': 'shape_id',
                'trip.headsign': 'headsign'
            },
            filters={
                'trip.system_id': context.system_id,
                'trip.trip_id': trip_id
            },
            limit=1,
            initializer=Trip.from_db
        )
        try:
            return trips[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context, route=None, block=None, limit=None) -> list[Trip]:
        '''Returns all trips that match the given context, route, and block'''
        route_id = getattr(route, 'id', route)
        block_id = getattr(block, 'id', block)
        return self.database.select('trip',
            columns={
                'trip.system_id': 'system_id',
                'trip.trip_id': 'id',
                'trip.route_id': 'route_id',
                'trip.service_id': 'service_id',
                'trip.block_id': 'block_id',
                'trip.direction_id': 'direction_id',
                'trip.shape_id': 'shape_id',
                'trip.headsign': 'headsign'
            },
            filters={
                'trip.system_id': context.system_id,
                'trip.route_id': route_id,
                'trip.block_id': block_id
            },
            limit=limit,
            initializer=Trip.from_db
        )
    
    def delete_all(self, context: Context):
        '''Deletes all trips for the given context from the database'''
        self.database.delete('trip', {
            'system_id': context.system_id
        })
