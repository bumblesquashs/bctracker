
from di import di

from models.context import Context
from models.direction import Direction
from models.time import Time

from repositories import DepartureRepository, PointRepository, SystemRepository

class Trip:
    '''A list of departures for a specific route and a specific service'''
    
    __slots__ = (
        'departure_repository',
        'point_repository',
        'context',
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
    def from_db(cls, row, prefix='trip', **kwargs):
        '''Returns a trip initialized from the given database row'''
        system_repository = kwargs.get('system_repository') or di[SystemRepository]
        system = system_repository.find(row[f'{prefix}_system_id'])
        context = Context(system=system)
        trip_id = row[f'{prefix}_id']
        route_id = row[f'{prefix}_route_id']
        service_id = row[f'{prefix}_service_id']
        block_id = row[f'{prefix}_block_id']
        direction_id = row[f'{prefix}_direction_id']
        shape_id = row[f'{prefix}_shape_id']
        headsign = row[f'{prefix}_headsign']
        return cls(context, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign)
    
    @property
    def url_id(self):
        '''The ID to use when making trip URLs'''
        return self.id
    
    @property
    def display_id(self):
        '''Formats the trip ID for web display'''
        return self.id.replace(':', ':<wbr />')
    
    @property
    def route(self):
        '''Returns the route associated with this trip'''
        return self.context.system.get_route(route_id=self.route_id)
    
    @property
    def block(self):
        '''Returns the block associated with this trip'''
        return self.context.system.get_block(self.block_id)
    
    @property
    def service(self):
        '''Returns the service associated with this trip'''
        return self.context.system.get_service(self.service_id)
    
    @property
    def first_stop(self):
        '''Returns the first stop of this trip'''
        departure = self.first_departure
        if departure:
            return departure.stop
        return None
    
    @property
    def last_stop(self):
        '''Returns the last stop of this trip'''
        departure = self.last_departure
        if departure:
            return departure.stop
        return None
    
    @property
    def start_time(self):
        '''Returns the time of the first departure of this trip'''
        departure = self.first_departure
        if departure:
            return departure.time
        return Time.unknown()
    
    @property
    def end_time(self):
        '''Returns the time of the last departure of this trip'''
        departure = self.last_departure
        if departure:
            return departure.time
        return Time.unknown()
    
    @property
    def duration(self):
        '''Returns the total time of this trip'''
        return self.start_time.format_difference(self.end_time)
    
    @property
    def length(self):
        '''Returns the distance travelled on this trip'''
        departure = self.last_departure
        if departure:
            return departure.distance
        return None
    
    @property
    def related_trips(self):
        '''Returns all trips with the same route, direction, start time, and end time as this trip'''
        if self._related_trips is None:
            self._related_trips = [t for t in self.context.system.get_trips() if self.is_related(t)]
            self._related_trips.sort(key=lambda t: t.service)
        return self._related_trips
    
    @property
    def cache(self):
        '''Returns the cache for this trip'''
        return self.context.system.get_trip_cache(self)
    
    @property
    def first_departure(self):
        '''Returns the first departure for this trip'''
        return self.cache.first_departure
    
    @property
    def last_departure(self):
        '''Returns the last departure for this trip'''
        return self.cache.last_departure
    
    @property
    def departure_count(self):
        '''Returns the departure count for this trip'''
        return self.cache.departure_count
    
    @property
    def direction(self):
        '''Returns the direction for this trip'''
        return self.cache.direction
    
    @property
    def custom_headsigns(self):
        '''Returns the custom headsigns for this trip'''
        return self.cache.custom_headsigns
    
    def __init__(self, context: Context, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign, **kwargs):
        self.context = context
        self.id = trip_id
        self.route_id = route_id
        self.service_id = service_id
        self.block_id = block_id
        self.direction_id = direction_id
        self.shape_id = shape_id
        self.headsign = headsign
        
        self.departure_repository = kwargs.get('departure_repository') or di[DepartureRepository]
        self.point_repository = kwargs.get('point_repository') or di[PointRepository]
        
        id_parts = trip_id.split(':')
        if len(id_parts) == 1:
            self.short_id = trip_id
        else:
            self.short_id = id_parts[0]
        
        self.sheets = context.system.copy_sheets([self.service])
        
        self._related_trips = None
    
    def __str__(self):
        if self.context.agency.prefix_headsigns and self.route:
            return f'{self.route.number} {self.headsign}'
        return self.headsign
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.start_time == other.start_time:
            return self.service < other.service
        return self.start_time < other.start_time
    
    def get_json(self):
        '''Returns a representation of this trip in JSON-compatible format'''
        json = {
            'shape_id': self.shape_id,
            'points': [p.get_json() for p in self.find_points()]
        }
        if self.route:
            json['colour'] = self.route.colour
            json['text_colour'] = self.route.text_colour
        else:
            json['colour'] = '666666'
            json['text_colour'] = '000000'
        return json
    
    def find_points(self):
        '''Returns all points associated with this trip'''
        return self.point_repository.find_all(self.context, self.shape_id)
    
    def find_departures(self):
        '''Returns all departures associated with this trip'''
        return self.departure_repository.find_all(self.context, trip=self)
    
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
    '''A collection of calculated values for a single trip'''
    
    __slots__ = (
        'first_departure',
        'last_departure',
        'departure_count',
        'direction',
        'custom_headsigns'
    )
    
    def __init__(self, departures):
        if departures:
            self.first_departure = departures[0]
            self.last_departure = departures[-1]
            self.departure_count = len(departures)
            self.direction = Direction.calculate(departures[0].stop, departures[-1].stop)
            headsigns = [str(d) for d in departures if d.headsign]
            previous_headsign = None
            self.custom_headsigns = []
            for headsign in headsigns:
                if headsign != previous_headsign:
                    self.custom_headsigns.append(headsign)
                previous_headsign = headsign
        else:
            self.first_departure = None
            self.last_departure = None
            self.departure_count = 0
            self.direction = Direction.UNKNOWN
            self.custom_headsigns = []
