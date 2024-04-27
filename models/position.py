
from di import di

from models.adherence import Adherence
from models.bus import Bus

from services import AgencyService, DepartureService, SystemService

class Position:
    '''Current information about a bus' coordinates, trip, and stop'''
    
    __slots__ = (
        'departure_service',
        'system',
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
        'adherence'
    )
    
    @classmethod
    def from_db(cls, row, prefix='position', **kwargs):
        '''Returns a position initialized from the given database row'''
        agency_service = kwargs.get('agency_service') or di[AgencyService]
        system_service = kwargs.get('system_service') or di[SystemService]
        agency = agency_service.find('bc-transit')
        system = system_service.find(row[f'{prefix}_system_id'])
        bus = Bus.find(agency, row[f'{prefix}_bus_number'])
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
            adherence = Adherence(adherence_value)
        return cls(system, bus, trip_id, stop_id, block_id, route_id, sequence, lat, lon, bearing, speed, adherence)
    
    @property
    def has_location(self):
        '''Checks if this position has non-null coordinates'''
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        '''Returns the trip associated with this position'''
        if not self.trip_id:
            return None
        return self.system.get_trip(self.trip_id)
    
    @property
    def stop(self):
        '''Returns the stop associated with this position'''
        if not self.stop_id:
            return None
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def block(self):
        '''Returns the block associated with this position'''
        if not self.block_id:
            return None
        return self.system.get_block(self.block_id)
    
    @property
    def route(self):
        '''Returns the route associated with this position'''
        if not self.route_id:
            return None
        return self.system.get_route(route_id=self.route_id)
    
    @property
    def colour(self):
        '''Returns the route colour associated with this position'''
        trip = self.trip
        if not trip:
            return '989898'
        return trip.route.colour
    
    @property
    def text_colour(self):
        '''Returns the route text colour associated with this position'''
        trip = self.trip
        if not trip:
            return 'FFFFFF'
        return trip.route.text_colour
    
    def __init__(self, system, bus, trip_id, stop_id, block_id, route_id, sequence, lat, lon, bearing, speed, adherence, **kwargs):
        self.system = system
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
        
        self.departure_service = kwargs.get('departure_service') or di[DepartureService]
    
    def __eq__(self, other):
        return self.bus == other.bus
    
    def __lt__(self, other):
        return self.bus < other.bus
    
    def get_json(self):
        '''Returns a representation of this position in JSON-compatible format'''
        data = {
            'bus_number': self.bus.number,
            'bus_display': str(self.bus),
            'system': str(self.system),
            'lon': self.lon,
            'lat': self.lat,
            'colour': self.colour,
            'text_colour': self.text_colour
        }
        order = self.bus.order
        if order:
            data['bus_order'] = str(order).replace("'", '&apos;')
            if order.model and order.model.type:
                data['bus_icon'] = f'bus-{order.model.type.name}'
            else:
                data['bus_icon'] = 'ghost'
        else:
            data['bus_order'] = 'Unknown Year/Model'
            data['bus_icon'] = 'ghost'
        if self.lon == 0 and self.lat == 0:
            data['bus_icon'] = 'fish'
        adornment = self.bus.find_adornment()
        if adornment and adornment.enabled:
            data['adornment'] = str(adornment)
        trip = self.trip
        if trip:
            data['headsign'] = str(trip).replace("'", '&apos;')
            data['route_number'] = trip.route.number
            data['system_id'] = trip.system.id
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
        return data
    
    def find_upcoming_departures(self):
        '''Returns the next 5 upcoming departures'''
        if not self.sequence or not self.trip:
            return []
        return self.departure_service.find_upcoming(self.system, self.trip, self.sequence)
