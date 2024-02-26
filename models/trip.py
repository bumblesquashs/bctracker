
import helpers.departure
import helpers.point
import helpers.system

from models.direction import Direction
from models.time import Time

class Trip:
    '''A list of departures for a specific route and a specific service'''
    
    __slots__ = (
        'system',
        'id',
        'short_id',
        'route_id',
        'service_id',
        'block_id',
        'direction_id',
        'shape_id',
        'headsign',
        'sheets',
        '_related_trips'
    )
    
    @classmethod
    def from_db(cls, row, prefix='trip'):
        system = helpers.system.find(row[f'{prefix}_system_id'])
        trip_id = row[f'{prefix}_id']
        route_id = row[f'{prefix}_route_id']
        service_id = row[f'{prefix}_service_id']
        block_id = row[f'{prefix}_block_id']
        direction_id = row[f'{prefix}_direction_id']
        shape_id = row[f'{prefix}_shape_id']
        headsign = row[f'{prefix}_headsign']
        return cls(system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign)
    
    @property
    def display_id(self):
        '''Formats the trip ID for web display'''
        return self.id.replace(':', ':<wbr />')
    
    @property
    def route(self):
        '''Returns the route associated with this trip'''
        return self.system.get_route(route_id=self.route_id)
    
    @property
    def block(self):
        '''Returns the block associated with this trip'''
        return self.system.get_block(self.block_id)
    
    @property
    def service(self):
        '''Returns the service associated with this trip'''
        return self.system.get_service(self.service_id)
    
    @property
    def first_stop(self):
        '''Returns the first stop of this trip'''
        departure = self.first_departure
        if departure is None:
            return None
        return departure.stop
    
    @property
    def last_stop(self):
        '''Returns the last stop of this trip'''
        departure = self.last_departure
        if departure is None:
            return None
        return departure.stop
    
    @property
    def start_time(self):
        '''Returns the time of the first departure of this trip'''
        departure = self.first_departure
        if departure is None:
            return Time.unknown()
        return departure.time
    
    @property
    def end_time(self):
        '''Returns the time of the last departure of this trip'''
        departure = self.last_departure
        if departure is None:
            return Time.unknown()
        return departure.time
    
    @property
    def duration(self):
        '''Returns the total time of this trip'''
        return self.start_time.format_difference(self.end_time)
    
    @property
    def length(self):
        '''Returns the distance travelled on this trip'''
        departure = self.last_departure
        if departure is None:
            return None
        return departure.distance
    
    @property
    def related_trips(self):
        '''Returns all trips with the same route, direction, start time, and end time as this trip'''
        if self._related_trips is None:
            self._related_trips = [t for t in self.system.get_trips() if self.is_related(t)]
            self._related_trips.sort(key=lambda t: t.service)
        return self._related_trips
    
    @property
    def cache(self):
        return self.system.get_trip_cache(self)
    
    @property
    def first_departure(self):
        return self.cache.first_departure
    
    @property
    def last_departure(self):
        return self.cache.last_departure
    
    @property
    def departure_count(self):
        return self.cache.departure_count
    
    @property
    def direction(self):
        return self.cache.direction
    
    def __init__(self, system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign):
        self.system = system
        self.id = trip_id
        self.route_id = route_id
        self.service_id = service_id
        self.block_id = block_id
        self.direction_id = direction_id
        self.shape_id = shape_id
        self.headsign = headsign
        
        id_parts = trip_id.split(':')
        if len(id_parts) == 1:
            self.short_id = trip_id
        else:
            self.short_id = id_parts[0]
        
        self.sheets = system.copy_sheets([self.service])
        
        self._related_trips = None
    
    def __str__(self):
        if self.system.agency.prefix_headsigns and self.route is not None:
            return f'{self.route.number} {self.headsign}'
        return self.headsign
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.start_time == other.start_time:
            return self.service < other.service
        return self.start_time < other.start_time
    
    def setup(self, departures=None):
        if self.is_setup:
            return
        self.is_setup = True
        if departures is None:
            departures = self.find_departures()
        if len(departures) == 0:
            return
    
    def get_json(self):
        '''Returns a representation of this trip in JSON-compatible format'''
        json = {
            'shape_id': self.shape_id,
            'points': [p.get_json() for p in self.find_points()]
        }
        if self.route is None:
            json['colour'] = '666666'
            json['text_colour'] = '000000'
        else:
            json['colour'] = self.route.colour
            json['text_colour'] = self.route.text_colour
        return json
    
    def find_points(self):
        '''Returns all points associated with this trip'''
        return helpers.point.find_all(self.system, self.shape_id)
    
    def find_departures(self):
        '''Returns all departures associated with this trip'''
        return helpers.departure.find_all(self.system, trip=self)
    
    def is_related(self, other):
        '''Checks if this trip has the same route, direction, start time, and end time as another trip'''
        if self.id == other.id:
            return False
        if self.route_id != other.route_id:
            return False
        if self.start_time != other.start_time:
            return False
        if self.end_time != other.end_time:
            return False
        if self.direction_id != other.direction_id:
            return False
        return True

class TripCache:
    
    __slots__ = (
        'first_departure',
        'last_departure',
        'departure_count',
        'direction'
    )
    
    def __init__(self, departures):
        self.first_departure = departures[0]
        self.last_departure = departures[-1]
        self.departure_count = len(departures)
        self.direction = Direction.calculate(departures[0].stop, departures[-1].stop)
