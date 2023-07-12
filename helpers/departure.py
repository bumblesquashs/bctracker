
from models.departure import Departure

import database

def create(departure):
    '''Inserts a new departure into the database'''
    database.insert('departure', {
        'system_id': departure.system.id,
        'trip_id': departure.trip_id,
        'sequence': departure.sequence,
        'stop_id': departure.stop_id,
        'time': departure.time.format_db(),
        'pickup_type': departure.pickup_type.value,
        'dropoff_type': departure.dropoff_type.value,
        'timepoint': 1 if departure.timepoint else 0,
        'distance': departure.distance
    })

def find(system_id, trip_id=None, sequence=None, stop_id=None):
    '''Returns the departure with the given system ID, trip ID, sequence, and stop ID'''
    departures = find_all(system_id, trip_id, sequence, stop_id)
    if len(departures) == 1:
        return departures[0]
    return None

def find_all(system_id, trip_id=None, sequence=None, stop_id=None, limit=None):
    '''Returns all departures that match the given system ID , trip ID, sequence, and stop ID'''
    if trip_id is not None:
        order_by = 'departure.sequence ASC'
    elif stop_id is not None:
        order_by = [
            'departure.time ASC',
            'departure.sequence DESC'
        ]
    else:
        order_by = None
    return database.select('departure',
        columns={
            'departure.system_id': 'departure_system_id',
            'departure.trip_id': 'departure_trip_id',
            'departure.sequence': 'departure_sequence',
            'departure.stop_id': 'departure_stop_id',
            'departure.time': 'departure_time',
            'departure.pickup_type': 'departure_pickup_type',
            'departure.dropoff_type': 'departure_dropoff_type',
            'departure.timepoint': 'departure_timepoint',
            'departure.distance': 'departure_distance'
        },
        filters={
            'departure.system_id': system_id,
            'departure.trip_id': trip_id,
            'departure.sequence': sequence,
            'departure.stop_id': stop_id
        },
        order_by=order_by,
        limit=limit,
        initializer=Departure.from_db)

def delete_all(system):
    '''Deletes all departures for the given system from the database'''
    database.delete('departure', {
        'system_id': system.id
    })
