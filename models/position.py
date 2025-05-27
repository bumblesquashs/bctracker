
from di import di

from models.adherence import Adherence
from models.bus import Bus
from models.context import Context
from models.occupancy import Occupancy
from models.timestamp import Timestamp

from repositories import DepartureRepository

class Position:
    '''Current information about a bus' coordinates, trip, and stop'''
    
    __slots__ = (
        'departure_repository',
        'context',
        'bus',
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
        'occupancy',
        'timestamp'
    )
    
    @classmethod
    def from_db(cls, row, prefix='position'):
        '''Returns a position initialized from the given database row'''
        context = Context.find(system_id=row[f'{prefix}_system_id'])
        bus = Bus.find(context, row[f'{prefix}_bus_number'])
        trip_id = row[f'{prefix}_trip_id']
        stop_id = row[f'{prefix}_stop_id']
        block_id = row[f'{prefix}_block_id']
        route_id = row[f'{prefix}_route_id']
        sequence = row[f'{prefix}_sequence']
        lat = row[f'{prefix}_lat']
        lon = row[f'{prefix}_lon']
        bearing = row[f'{prefix}_bearing']
        speed = row[f'{prefix}_speed']
        adherence_value = row[f'{prefix}_adherence']
        if adherence_value is None:
            adherence = None
        else:
            trip = context.system.get_trip(trip_id)
            layover = sequence is not None and trip and trip.first_departure.sequence == sequence and adherence_value > 0
            adherence = Adherence(adherence_value, layover)
        try:
            occupancy = Occupancy[row[f'{prefix}_occupancy']]
        except KeyError:
            occupancy = Occupancy.NO_DATA_AVAILABLE
        timestamp = Timestamp.parse(row[f'{prefix}_timestamp'], timezone=context.timezone)
        return cls(context, bus, trip_id, stop_id, block_id, route_id, sequence, lat, lon, bearing, speed, adherence, occupancy, timestamp)
    
    @property
    def has_location(self):
        '''Checks if this position has non-null coordinates'''
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        '''Returns the trip associated with this position'''
        if self.trip_id:
            return self.context.system.get_trip(self.trip_id)
        return None
    
    @property
    def stop(self):
        '''Returns the stop associated with this position'''
        if self.stop_id:
            return self.context.system.get_stop(stop_id=self.stop_id)
        return None
    
    @property
    def block(self):
        '''Returns the block associated with this position'''
        if not self.block_id:
            return self.context.system.get_block(self.block_id)
        return None
    
    @property
    def route(self):
        '''Returns the route associated with this position'''
        if not self.route_id:
            return self.context.system.get_route(route_id=self.route_id)
        return None
    
    @property
    def colour(self):
        '''Returns the route colour associated with this position'''
        trip = self.trip
        if trip and trip.route:
            return trip.route.colour
        return '989898'
    
    @property
    def text_colour(self):
        '''Returns the route text colour associated with this position'''
        trip = self.trip
        if trip and trip.route:
            return trip.route.text_colour
        return 'FFFFFF'
    
    @property
    def departure(self):
        '''Returns the departure associated with this position'''
        return self.departure_repository.find(self.context, self.trip_id, self.sequence)
    
    def __init__(self, context: Context, bus, trip_id, stop_id, block_id, route_id, sequence, lat, lon, bearing, speed, adherence, occupancy, timestamp, **kwargs):
        self.context = context
        self.bus = bus
        self.trip_id = trip_id
        self.stop_id = stop_id
        self.block_id = block_id
        self.route_id = route_id
        self.sequence = sequence
        self.lat = lat
        self.lon = lon
        self.bearing = bearing
        self.speed = speed
        self.adherence = adherence
        self.occupancy = occupancy
        self.timestamp = timestamp
        
        self.departure_repository = kwargs.get('departure_repository') or di[DepartureRepository]
    
    def __eq__(self, other):
        return self.bus == other.bus
    
    def __lt__(self, other):
        return self.bus < other.bus
    
    def get_json(self):
        '''Returns a representation of this position in JSON-compatible format'''
        data = {
            'bus_number': self.bus.number,
            'bus_display': str(self.bus),
            'bus_url_id': str(self.bus.url_id),
            'system': str(self.context.system),
            'agency_id': self.context.agency_id,
            'lon': self.lon,
            'lat': self.lat,
            'colour': self.colour,
            'text_colour': self.text_colour,
            'occupancy_name': self.occupancy.value,
            'occupancy_status_class': self.occupancy.status_class,
            'occupancy_icon': self.occupancy.icon
        }
        order = self.bus.order
        if order:
            data['bus_order'] = str(order).replace("'", '&apos;')
            if order.model and order.model.type:
                data['bus_icon'] = f'model/type/bus-{order.model.type.name}'
            else:
                data['bus_icon'] = 'ghost'
        else:
            data['bus_order'] = 'Unknown Year/Model'
            data['bus_icon'] = 'ghost'
        adornment = self.bus.find_adornment()
        if adornment and adornment.enabled:
            data['adornment'] = str(adornment)
        trip = self.trip
        if trip:
            departure = self.departure
            if departure and departure.headsign:
                data['headsign'] = str(departure).replace("'", '&apos;')
            else:
                data['headsign'] = str(trip).replace("'", '&apos;')
            data['route_number'] = trip.route.number
            data['system_id'] = trip.context.system_id
            data['shape_id'] = trip.shape_id
        else:
            data['headsign'] = 'Not In Service'
            data['route_number'] = 'NIS'
        bearing = self.bearing
        if bearing is not None:
            data['bearing'] = bearing
        speed = self.speed
        if speed is not None:
            data['speed'] = speed
        adherence = self.adherence
        if adherence:
            data['adherence'] = adherence.get_json()
        timestamp = self.timestamp
        if timestamp:
            data['timestamp'] = timestamp.value
        return data
    
    def find_upcoming_departures(self):
        '''Returns the trip's upcoming departures'''
        if self.sequence is None or not self.trip:
            return []
        return self.departure_repository.find_upcoming(self.context, self.trip, self.sequence)
