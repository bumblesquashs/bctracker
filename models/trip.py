
from enum import Enum

from datetime import datetime

import helpers.point

from models.time import Time

class Direction(Enum):
    '''A basic description of the path a trip follows'''
    
    CIRCULAR = 'Circular'
    SOUTHBOUND = 'Southbound'
    NORTHBOUND = 'Northbound'
    WESTBOUND = 'Westbound'
    EASTBOUND = 'Eastbound'
    UNKNOWN = 'Unknown'
    
    def __str__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value

class Trip:
    '''A list of departures for a specific route and a specific service'''
    
    __slots__ = ('system', 'id', 'route_id', 'service_id', 'block_id', 'direction_id', 'shape_id', 'headsign', 'departures', 'direction', 'sheets', '_related_trips')
    
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
        self.departures = departures
        
        if len(departures) == 0:
            self.direction = Direction.UNKNOWN
        else:
            first_stop = self.first_departure.stop
            last_stop = self.last_departure.stop
            lat_diff = first_stop.lat - last_stop.lat
            lon_diff = first_stop.lon - last_stop.lon
            if abs(lat_diff) <= 0.001 and abs(lon_diff) <= 0.001:
                self.direction = Direction.CIRCULAR
            elif abs(lat_diff) > abs(lon_diff):
                self.direction = Direction.SOUTHBOUND if lat_diff > 0 else Direction.NORTHBOUND
            elif abs(lon_diff) > abs(lat_diff):
                self.direction = Direction.WESTBOUND if lon_diff > 0 else Direction.EASTBOUND
            else:
                self.direction = Direction.UNKNOWN
        
        self.sheets = system.copy_sheets([self.service])
        
        self._related_trips = None
    
    def __str__(self):
        if self.system.prefix_headsign and self.route is not None:
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
    def stops(self):
        '''Returns all stops associated with this trip'''
        return {d.stop for d in self.departures}
    
    @property
    def first_departure(self):
        '''Returns the first departure of this trip'''
        if len(self.departures) == 0:
            return None
        return self.departures[0]
    
    @property
    def last_departure(self):
        '''Returns the last departure of this trip'''
        if len(self.departures) == 0:
            return None
        return self.departures[-1]
    
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
        return departure.distance_traveled
    
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
        json = {
            'shape_id': self.shape_id,
            'points': [p.json for p in self.load_points()]
        }
        if self.route is None:
            json['colour'] = '666666'
            json['text_colour'] = '000000'
        else:
            json['colour'] = self.route.colour
            json['text_colour'] = self.route.text_colour
        return json
    
    def load_points(self):
        '''Returns all points associated with this trip'''
        return helpers.point.find_all(self.system.id, self.shape_id)
    
    def get_departure(self, stop):
        '''Returns the departure for a given stop on this trip'''
        departures = [d for d in self.departures if d.stop == stop]
        if len(departures) == 0:
            return None
        if len(departures) == 1:
            return departures[0]
        now = datetime.now()
        current_mins = (now.hour * 60) + now.minute
        departures.sort(key=lambda d: abs(current_mins - d.time.get_minutes()))
        return departures[0]
    
    def get_previous_departure(self, departure):
        '''Returns the departure in this trip that comes before the given departure'''
        for previous_departure in self.departures:
            if previous_departure.sequence == (departure.sequence - 1):
                return previous_departure
        return None
    
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
