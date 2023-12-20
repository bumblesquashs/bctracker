
from models.trip import Trip

import database

def create(system, row):
    '''Inserts a new trip into the database'''
    system_id = getattr(system, 'id', system)
    database.insert('trip', {
        'system_id': system_id,
        'trip_id': row['trip_id'],
        'route_id': row['route_id'],
        'service_id': row['service_id'],
        'block_id': row['block_id'],
        'direction_id': int(row['direction_id']),
        'shape_id': row['shape_id'],
        'headsign': row['trip_headsign']
    })

def find(system, trip_id):
    '''Returns the trip with the given system and trip ID'''
    system_id = getattr(system, 'id', system)
    trips = database.select('trip',
        columns={
            'trip.system_id': 'trip_system_id',
            'trip.trip_id': 'trip_id',
            'trip.route_id': 'trip_route_id',
            'trip.service_id': 'trip_service_id',
            'trip.block_id': 'trip_block_id',
            'trip.direction_id': 'trip_direction_id',
            'trip.shape_id': 'trip_shape_id',
            'trip.headsign': 'trip_headsign'
        },
        filters={
            'trip.system_id': system_id,
            'trip.trip_id': trip_id
        },
        limit=1,
        initializer=Trip.from_db
    )
    if len(trips) == 0:
        return None
    return trips[0]

def find_all(system, route=None, block=None, limit=None):
    '''Returns all trips that match the given system, route, and block'''
    system_id = getattr(system, 'id', system)
    route_id = getattr(route, 'id', route)
    block_id = getattr(block, 'id', block)
    return database.select('trip',
        columns={
            'trip.system_id': 'trip_system_id',
            'trip.trip_id': 'trip_id',
            'trip.route_id': 'trip_route_id',
            'trip.service_id': 'trip_service_id',
            'trip.block_id': 'trip_block_id',
            'trip.direction_id': 'trip_direction_id',
            'trip.shape_id': 'trip_shape_id',
            'trip.headsign': 'trip_headsign'
        },
        filters={
            'trip.system_id': system_id,
            'trip.route_id': route_id,
            'trip.block_id': block_id
        },
        limit=limit,
        initializer=Trip.from_db
    )

def delete_all(system):
    '''Deletes all trips for the given system from the database'''
    system_id = getattr(system, 'id', system)
    database.delete('trip', {
        'system_id': system_id
    })
