
from database import Database

from protobuf.data.gtfs_realtime_pb2 import _VEHICLEPOSITION_OCCUPANCYSTATUS

from models.adherence import Adherence
from models.context import Context
from models.occupancy import Occupancy
from models.position import Position
from models.timestamp import Timestamp

class PositionRepository:
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database: Database):
        self.database = database
    
    def create(self, context: Context, bus, data):
        '''Inserts a new position into the database'''
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
        trip = context.system.get_trip(trip_id)
        stop = context.system.get_stop(stop_id=stop_id)
        if trip:
            block_id = trip.block_id
            route_id = trip.route_id
        else:
            block_id = None
            route_id = None
        try:
            if data.HasField('timestamp'):
                timestamp = Timestamp.parse(data.timestamp, context.timezone)
            else:
                timestamp = None
        except AttributeError:
            timestamp = None
        if trip and stop and sequence is not None and lat is not None and lon is not None:
            adherence = Adherence.calculate(trip, stop, sequence, lat, lon, timestamp)
        else:
            adherence = None
        try:
            if data.HasField('occupancy_status'):
                value = _VEHICLEPOSITION_OCCUPANCYSTATUS.values_by_number[data.occupancy_status]
                occupancy = Occupancy[value.name]
            else:
                occupancy = Occupancy.NO_DATA_AVAILABLE
        except KeyError:
            occupancy = Occupancy.NO_DATA_AVAILABLE
        values = {
            'system_id': context.system_id,
            'bus_number': bus_number,
            'trip_id': trip_id,
            'stop_id': stop_id,
            'block_id': block_id,
            'route_id': route_id,
            'sequence': sequence,
            'lat': lat,
            'lon': lon,
            'bearing': bearing,
            'speed': speed,
            'occupancy': occupancy.name
        }
        if adherence:
            values['adherence'] = adherence.value
        if timestamp:
            values['timestamp'] = timestamp.value
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
                'position.adherence': 'position_adherence',
                'position.occupancy': 'position_occupancy',
                'position.timestamp': 'position_timestamp'
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
    
    def find_all(self, context: Context = Context(), trip=None, stop=None, block=None, route=None, has_location=None):
        '''Returns all positions that match the given system, trip, stop, block, and route'''
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
            'position.system_id': context.system_id,
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
                'position.adherence': 'position_adherence',
                'position.occupancy': 'position_occupancy',
                'position.timestamp': 'position_timestamp'
            },
            filters=filters,
            initializer=Position.from_db
        )
        return [p for p in positions if p.bus.visible]
    
    def delete_all(self, context: Context = Context()):
        '''Deletes all positions for the given system from the database'''
        self.database.delete('position', {
            'position.system_id': context.system_id
        })
