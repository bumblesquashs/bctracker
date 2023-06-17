
import helpers.departure
import helpers.point

from models.direction import Direction
from models.time import Time

class Trip:
    '''A list of departures for a specific route and a specific service'''
    
    __slots__ = ('system', 'id', 'route_id', 'service_id', 'block_id', 'direction_id', 'shape_id', 'headsign', 'first_departure', 'last_departure', 'departure_count', 'direction', '_related_trips')
    
    @classmethod
    def from_csv(cls, row, system, departures):
        '''Returns a trip initialized from the given CSV row'''
        trip_id = row['trip_id']
        route_id = row['route_id']
        service_id = row['service_id']
        block_id = row['block_id']
        direction_id = int(row['direction_id'])
        shape_id = row['shape_id']
        headsign = row['trip_headsign']
        return cls(system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign, sorted(departures.get(trip_id, [])))
    
    def __init__(self, system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign, departures):
        self.system = system
        self.id = trip_id
        self.route_id = route_id
        self.service_id = service_id
        self.block_id = block_id
        self.direction_id = direction_id
        self.shape_id = shape_id
        self.headsign = headsign
        self.departure_count = len(departures)
        
        if len(departures) == 0:
            self.first_departure = None
            self.last_departure = None
            self.direction = Direction.UNKNOWN
        else:
            self.first_departure = departures[0]
            self.last_departure = departures[-1]
            self.direction = Direction.calculate(self.first_stop, self.last_stop)
        
        self._related_trips = None
    
    def __str__(self):
        if self.system.prefix_headsign:
            return f'{self.route.number} {self.headsign}'
        return self.headsign
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.start_time == other.start_time:
            return self.service < other.service
        return self.start_time < other.start_time
    
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
    def json(self):
        '''Returns a representation of this trip in JSON-compatible format'''
        return {
            'shape_id': self.shape_id,
            'colour': self.route.colour,
            'text_colour': self.route.text_colour,
            'points': [p.json for p in self.load_points()]
        }
    
    def load_points(self):
        '''Returns all points associated with this trip'''
        return helpers.point.find_all(self.system.id, self.shape_id)
    
    def load_departures(self):
        '''Returns all departures associated with this trip'''
        return helpers.departure.find_all(self.system.id, trip_id=self.id)
    
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
