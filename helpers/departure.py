
from models.departure import Departure, PickupType, DropoffType

import database

class DepartureService:
    
    def create(self, system, row):
        '''Inserts a new departure into the database'''
        system_id = getattr(system, 'id', system)
        try:
            pickup_type = PickupType(row['pickup_type'])
        except (KeyError, ValueError):
            pickup_type = PickupType.NORMAL
        try:
            dropoff_type = DropoffType(row['drop_off_type'])
        except (KeyError, ValueError):
            dropoff_type = DropoffType.NORMAL
        try:
            timepoint = row['timepoint'] == '1'
        except KeyError:
            timepoint = False
        try:
            distance = int(row['shape_dist_traveled'])
        except (KeyError, ValueError):
            distance = None
        database.insert('departure', {
            'system_id': system_id,
            'trip_id': row['trip_id'],
            'sequence': int(row['stop_sequence']),
            'stop_id': row['stop_id'],
            'time': row['departure_time'],
            'pickup_type': pickup_type.value,
            'dropoff_type': dropoff_type.value,
            'timepoint': 1 if timepoint else 0,
            'distance': distance
        })
    
    def find(self, system, trip=None, sequence=None, stop=None):
        '''Returns the departure with the given system, trip, sequence, and stop'''
        departures = self.find_all(system, trip, sequence, stop)
        if len(departures) == 1:
            return departures[0]
        return None
    
    def find_all(self, system, trip=None, sequence=None, route=None, stop=None, block=None, limit=None):
        '''Returns all departures that match the given system, trip, sequence, and stop'''
        system_id = getattr(system, 'id', system)
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
                'trip.trip_id': 'departure.trip_id'
            }
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
            joins=joins,
            filters={
                'departure.system_id': system_id,
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
    
    def find_upcoming(self, system, trip, sequence, limit=5):
        '''Returns all departures on a trip from the given sequence number onwards'''
        system_id = getattr(system, 'id', system)
        trip_id = getattr(trip, 'id', trip)
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
                'departure.sequence': {
                    '>=': sequence
                }
            },
            order_by='departure.sequence',
            limit=limit,
            initializer=Departure.from_db
        )
    
    def find_adjacent(self, system, stop):
        '''Returns all departures on trips that serve the given stop'''
        system_id = getattr(system, 'id', system)
        stop_id = getattr(stop, 'id', stop)
        cte, args = database.build_select('departure',
            columns='trip.*',
            joins={
                'trip': {
                    'trip.system_id': 'departure.system_id',
                    'trip.trip_id': 'departure.trip_id'
                }
            },
            filters={
                'departure.system_id': system_id,
                'departure.stop_id': stop_id
            })
        return database.select('stop_trip',
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
            ctes={
                'stop_trip': cte
            },
            joins={
                'departure': {
                    'departure.system_id': 'stop_trip.system_id',
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
    
    def delete_all(self, system):
        '''Deletes all departures for the given system from the database'''
        system_id = getattr(system, 'id', system)
        database.delete('departure', {
            'system_id': system_id
        })

default = DepartureService()
