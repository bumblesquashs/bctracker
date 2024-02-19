
from models.departure import Departure, PickupType, DropoffType

import database

def create(system, agency, row):
    '''Inserts a new departure into the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    if 'pickup_type' in row:
        pickup_type = PickupType(row['pickup_type'])
    else:
        pickup_type = PickupType.NORMAL
    if 'drop_off_type' in row:
        dropoff_type = DropoffType(row['drop_off_type'])
    else:
        dropoff_type = DropoffType.NORMAL
    if 'timepoint' in row:
        timepoint = row['timepoint'] == '1'
    else:
        timepoint = False
    if 'shape_dist_traveled' in row:
        try:
            distance = int(row['shape_dist_traveled'])
        except:
            distance = None
    else:
        distance = None
    database.insert('departure', {
        'system_id': system_id,
        'agency_id': agency_id,
        'trip_id': row['trip_id'],
        'sequence': int(row['stop_sequence']),
        'stop_id': row['stop_id'],
        'time': row['departure_time'],
        'pickup_type': pickup_type.value,
        'dropoff_type': dropoff_type.value,
        'timepoint': 1 if timepoint else 0,
        'distance': distance
    })

def find(system, agency, trip=None, sequence=None, stop=None):
    '''Returns the departure with the given trip, sequence, and stop'''
    departures = find_all(system, agency, trip, sequence, stop)
    if len(departures) == 1:
        return departures[0]
    return None

def find_all(system, agency, trip=None, sequence=None, route=None, stop=None, block=None, limit=None):
    '''Returns all departures that match the given trip, sequence, and stop'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    trip_id = getattr(trip, 'id', trip)
    route_id = getattr(route, 'id', route)
    stop_id = getattr(stop, 'id', stop)
    block_id = getattr(block, 'id', block)
    if trip_id is not None:
        order_by = 'departure.sequence ASC'
    elif stop_id is not None:
        order_by = [
            'departure.time ASC',
            'departure.sequence DESC'
        ]
    else:
        order_by = None
    joins = {}
    if route_id is not None or block_id is not None:
        joins['trip'] = {
            'trip.system_id': 'departure.system_id',
            'trip.agency_id': 'departure.agency_id',
            'trip.trip_id': 'departure.trip_id'
        }
    return database.select('departure',
        columns={
            'departure.system_id': 'departure_system_id',
            'departure.agency_id': 'departure_agency_id',
            'departure.trip_id': 'departure_trip_id',
            'departure.sequence': 'departure_sequence',
            'departure.stop_id': 'departure_stop_id',
            'departure.time': 'departure_time',
            'departure.pickup_type': 'departure_pickup_type',
            'departure.dropoff_type': 'departure_dropoff_type',
            'departure.timepoint': 'departure_timepoint',
            'departure.distance': 'departure_distance'
        },
        joins=joins,
        filters={
            'departure.system_id': system_id,
            'departure.agency_id': agency_id,
            'departure.trip_id': trip_id,
            'departure.sequence': sequence,
            'departure.stop_id': stop_id,
            'trip.block_id': block_id,
            'trip.route_id': route_id
        },
        order_by=order_by,
        limit=limit,
        initializer=Departure.from_db
    )

def find_upcoming(system, agency, trip, sequence, limit=5):
    '''Returns all departures on a trip from the given sequence number onwards'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    trip_id = getattr(trip, 'id', trip)
    return database.select('departure',
        columns={
            'departure.system_id': 'departure_system_id',
            'departure.agency_id': 'departure_agency_id',
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
            'departure.agency_id': agency_id,
            'departure.trip_id': trip_id,
            'departure.sequence': {
                '>=': sequence
            }
        },
        order_by='departure.sequence',
        limit=limit,
        initializer=Departure.from_db
    )

def find_adjacent(system, agency, stop):
    '''Returns all departures on trips that serve the given stop'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    stop_id = getattr(stop, 'id', stop)
    cte, args = database.build_select('departure',
        columns='trip.*',
        joins={
            'trip': {
                'trip.system_id': 'departure.system_id',
                'trip.agency_id': 'departure.agency_id',
                'trip.trip_id': 'departure.trip_id'
            }
        },
        filters={
            'departure.system_id': system_id,
            'departure.agency_id': agency_id,
            'departure.stop_id': stop_id
        })
    return database.select('stop_trip',
        columns={
            'departure.system_id': 'departure_system_id',
            'departure.agency_id': 'departure_agency_id',
            'departure.trip_id': 'departure_trip_id',
            'departure.sequence': 'departure_sequence',
            'departure.stop_id': 'departure_stop_id',
            'departure.time': 'departure_time',
            'departure.pickup_type': 'departure_pickup_type',
            'departure.dropoff_type': 'departure_dropoff_type',
            'departure.timepoint': 'departure_timepoint',
            'departure.distance': 'departure_distance'
        },
        ctes={
            'stop_trip': cte
        },
        joins={
            'departure': {
                'departure.system_id': 'stop_trip.system_id',
                'departure.agency_id': 'stop_trip.agency_id',
                'departure.trip_id': 'stop_trip.trip_id'
            }
        },
        filters={
            'departure.stop_id': {
                '!=': stop_id
            }
        },
        custom_args=args,
        initializer=Departure.from_db
    )

def delete_all(system, agency):
    '''Deletes all departures from the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    database.delete('departure', {
        'system_id': system_id,
        'agency_id': agency_id
    })
