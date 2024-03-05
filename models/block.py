
import helpers.departure

from models.match import Match
from models.schedule import Schedule
from models.time import Time

class Block:
    '''A list of trips that are operated by the same bus sequentially'''
    
    __slots__ = (
        'system',
        'agency',
        'id',
        'trips',
        'schedule',
        'sheets',
        '_related_blocks'
    )
    
    @property
    def related_blocks(self):
        '''Returns all blocks that have the same start time, end time, and routes as this block'''
        if self._related_blocks is None:
            related_blocks = [b for b in self.system.get_blocks() if self.is_related(b)]
            self._related_blocks = sorted(related_blocks, key=lambda b: b.schedule)
        return self._related_blocks
    
    def __init__(self, system, agency, id, trips):
        self.system = system
        self.agency = agency
        self.id = id
        self.trips = trips
        
        services = {t.service for t in trips}
        self.schedule = Schedule.combine(services)
        self.sheets = system.copy_sheets(services)
        
        self._related_blocks = None
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    def get_trips(self, service_group=None, date=None):
        '''Returns all trips from this block'''
        if service_group is None:
            if date is None:
                return sorted(self.trips)
            return sorted([t for t in self.trips if date in t.service])
        return sorted([t for t in self.trips if t.service in service_group])
    
    def get_routes(self, service_group=None, date=None):
        '''Returns all routes from this block'''
        return sorted({t.route for t in self.get_trips(service_group, date)})
    
    def get_routes_string(self, service_group=None, date=None):
        '''Returns a string of all routes from this block'''
        return ', '.join([r.number for r in self.get_routes(service_group, date)])
    
    def get_start_time(self, service_group=None, date=None):
        '''Returns the start time of this block'''
        trips = self.get_trips(service_group, date)
        if len(trips) == 0:
            return Time.unknown()
        return trips[0].start_time
    
    def get_end_time(self, service_group=None, date=None):
        '''Returns the end time of this block'''
        trips = self.get_trips(service_group, date)
        if len(trips) == 0:
            return Time.unknown()
        return trips[-1].end_time
    
    def get_duration(self, service_group=None, date=None):
        '''Returns the duration of this block'''
        start_time = self.get_start_time(service_group, date)
        end_time = self.get_end_time(service_group, date)
        return start_time.format_difference(end_time)
    
    def is_related(self, other):
        '''Checks if this block has the same start time, end time, and routes as another block'''
        if self.id == other.id:
            return False
        if self.get_routes() != other.get_routes():
            return False
        if self.get_start_time() != other.get_start_time():
            return False
        if self.get_end_time() != other.get_end_time():
            return False
        return True
    
    def get_match(self, query):
        '''Returns a match for this block with the given query'''
        query = query.lower()
        id = self.id
        value = 0
        if query in id:
            value += (len(query) / len(id)) * 100
            if id.startswith(query):
                value += len(query)
        routes = self.get_routes_string()
        if routes.count(',') == 0:
            message = f'Route {routes}'
        else:
            message = f'Routes {routes}'
        return Match(f'Block {id}', message, 'block', f'/blocks/{self.id}', value)
    
    def find_departures(self):
        '''Returns all departures for this block'''
        return helpers.departure.find_all(self.system, self.agency, block=self)
