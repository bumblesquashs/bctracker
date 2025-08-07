
from dataclasses import dataclass

from database import Database

from protobuf.data.gtfs_realtime_pb2 import _VEHICLEPOSITION_OCCUPANCYSTATUS

from models.adherence import Adherence
from models.context import Context
from models.occupancy import Occupancy
from models.position import Position
from models.timestamp import Timestamp

@dataclass(slots=True)
class PositionRepository:
    
    database: Database
    
    def create(self, context: Context, vehicle_id: str, data):
        '''Inserts a new position into the database'''
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
            'agency_id': context.agency_id,
            'vehicle_id': vehicle_id,
            'system_id': context.system_id,
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
            values['layover'] = 1 if adherence.layover else 0
        if timestamp:
            values['timestamp'] = timestamp.value
        self.database.insert('position', values)
    
    def find(self, agency_id: str, vehicle_id: str) -> Position | None:
        '''Returns the position of the given bus'''
        positions = self.database.select(
            table='position',
            columns=[
                'agency_id',
                'vehicle_id',
                'system_id',
                'trip_id',
                'stop_id',
                'block_id',
                'route_id',
                'sequence',
                'lat',
                'lon',
                'bearing',
                'speed',
                'adherence',
                'layover',
                'occupancy',
                'timestamp'
            ],
            filters={
                'agency_id': agency_id,
                'vehicle_id': vehicle_id
            },
            initializer=Position.from_db
        )
        try:
            return positions[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context = Context(), trip_id: str | list[str] | None = None, stop_id: str | list[str] | None = None, block_id: str | list[str] | None = None, route_id: str | list[str] | None = None, has_location: bool | None = None) -> list[Position]:
        '''Returns all positions that match the given system, trip, stop, block, and route'''
        filters = {
            'agency_id': context.agency_id,
            'system_id': context.system_id,
            'trip_id': trip_id,
            'stop_id': stop_id,
            'block_id': block_id,
            'route_id': route_id
        }
        if has_location is not None:
            if has_location:
                filters['lat'] = {
                    'IS NOT': None
                }
                filters['lon'] = {
                    'IS NOT': None
                }
            else:
                filters['lat'] = {
                    'IS': None
                }
                filters['lon'] = {
                    'IS': None
                }
        positions = self.database.select(
            table='position',
            columns=[
                'agency_id',
                'vehicle_id',
                'system_id',
                'trip_id',
                'stop_id',
                'block_id',
                'route_id',
                'sequence',
                'lat',
                'lon',
                'bearing',
                'speed',
                'adherence',
                'layover',
                'occupancy',
                'timestamp'
            ],
            filters=filters,
            initializer=Position.from_db
        )
        return [p for p in positions if p.bus.visible]
    
    def delete_all(self, context: Context = Context()):
        '''Deletes all positions for the given system from the database'''
        self.database.delete(
            table='position',
            filters={
                'agency_id': context.agency_id,
                'system_id': context.system_id
            }
        )
