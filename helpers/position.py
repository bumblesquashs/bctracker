
from di import di

from models.adherence import Adherence
from models.position import Position

from database import Database

class PositionService:
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database=di[Database]):
        self.database = database
    
    def create(self, system, bus, data):
        '''Inserts a new position into the database'''
        system_id = getattr(system, 'id', system)
        bus_number = getattr(bus, 'number', bus)
        try:
            trip_id = data.trip.trip_id
            if trip_id == '':
                trip_id = None
        except AttributeError:
            trip_id = None
        try:
            stop_id = data.stop_id
            if stop_id == '':
                stop_id = None
        except AttributeError:
            stop_id = None
        try:
            if data.HasField('current_stop_sequence'):
                sequence = int(data.current_stop_sequence)
            else:
                sequence = None
        except:
            sequence = None
        try:
            lat = data.position.latitude
            lon = data.position.longitude
        except AttributeError:
            lat = None
            lon = None
        try:
            if data.position.HasField('bearing'):
                bearing = data.position.bearing
            else:
                bearing = None
        except AttributeError:
            bearing = None
        try:
            speed = int(data.position.speed * 3.6)
        except AttributeError:
            speed = None
        trip = system.get_trip(trip_id)
        stop = system.get_stop(stop_id=stop_id)
        if trip is None:
            block_id = None
            route_id = None
        else:
            block_id = trip.block_id
            route_id = trip.route_id
        if trip is None or stop is None or sequence is None or lat is None or lon is None:
            adherence = None
        else:
            adherence = Adherence.calculate(trip, stop, sequence, lat, lon)
        values = {
            'system_id': system_id,
            'bus_number': bus_number,
            'trip_id': trip_id,
            'stop_id': stop_id,
            'block_id': block_id,
            'route_id': route_id,
            'sequence': sequence,
            'lat': lat,
            'lon': lon,
            'bearing': bearing,
            'speed': speed
        }
        if adherence:
            values['adherence'] = adherence.value
        self.database.insert('position', values)
    
    def find(self, bus):
        '''Returns the position of the given bus'''
        bus_number = getattr(bus, 'number', bus)
        positions = self.database.select('position',
            columns={
                'position.system_id': 'position_system_id',
                'position.bus_number': 'position_bus_number',
                'position.trip_id': 'position_trip_id',
                'position.stop_id': 'position_stop_id',
                'position.block_id': 'position_block_id',
                'position.route_id': 'position_route_id',
                'position.sequence': 'position_sequence',
                'position.lat': 'position_lat',
                'position.lon': 'position_lon',
                'position.bearing': 'position_bearing',
                'position.speed': 'position_speed',
                'position.adherence': 'position_adherence'
            },
            filters={
                'position.bus_number': bus_number
            },
            initializer=Position.from_db
        )
        try:
            return positions[0]
        except IndexError:
            return None
    
    def find_all(self, system=None, trip=None, stop=None, block=None, route=None, has_location=None):
        '''Returns all positions that match the given system, trip, stop, block, and route'''
        system_id = getattr(system, 'id', system)
        if isinstance(trip, list):
            trip_id = [getattr(t, 'id', t) for t in trip]
        else:
            trip_id = getattr(trip, 'id', trip)
        if isinstance(stop, list):
            stop_id = [getattr(s, 'id', s) for s in stop]
        else:
            stop_id = getattr(stop, 'id', stop)
        if isinstance(block, list):
            block_id = [getattr(b, 'id', b) for b in block]
        else:
            block_id = getattr(block, 'id', block)
        if isinstance(route, list):
            route_id = [getattr(r, 'id', r) for r in route]
        else:
            route_id = getattr(route, 'id', route)
        filters = {
            'position.system_id': system_id,
            'position.trip_id': trip_id,
            'position.stop_id': stop_id,
            'position.block_id': block_id,
            'position.route_id': route_id
        }
        if has_location is not None:
            if has_location:
                filters['position.lat'] = {
                    'IS NOT': None
                }
                filters['position.lon'] = {
                    'IS NOT': None
                }
            else:
                filters['position.lat'] = {
                    'IS': None
                }
                filters['position.lon'] = {
                    'IS': None
                }
        positions = self.database.select('position',
            columns={
                'position.system_id': 'position_system_id',
                'position.bus_number': 'position_bus_number',
                'position.trip_id': 'position_trip_id',
                'position.stop_id': 'position_stop_id',
                'position.block_id': 'position_block_id',
                'position.route_id': 'position_route_id',
                'position.sequence': 'position_sequence',
                'position.lat': 'position_lat',
                'position.lon': 'position_lon',
                'position.bearing': 'position_bearing',
                'position.speed': 'position_speed',
                'position.adherence': 'position_adherence'
            },
            filters=filters,
            initializer=Position.from_db
        )
        return [p for p in positions if p.bus.visible]
    
    def delete_all(self, system=None):
        '''Deletes all positions for the given system from the database'''
        system_id = getattr(system, 'id', system)
        self.database.delete('position', {
            'position.system_id': system_id
        })

default = PositionService()
