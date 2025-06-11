
from dataclasses import dataclass, field

from models.context import Context
from models.match import Match
from models.schedule import Schedule
from models.time import Time

@dataclass(slots=True)
class Block:
    '''A list of trips that are operated by the same bus sequentially'''
    
    context: Context
    id: str
    trips: list
    
    schedule: Schedule = field(init=False)
    sheets: list = field(init=False)
    
    @property
    def url_id(self):
        '''The ID to use when making block URLs'''
        return self.id
    
    def __post_init__(self):
        services = {t.service for t in self.trips}
        self.schedule = Schedule.combine(services)
        self.sheets = self.context.system.copy_sheets(services)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    def get_trips(self, service_group=None, date=None):
        '''Returns all trips from this block'''
        if service_group:
            return sorted([t for t in self.trips if t.service in service_group])
        if date:
            return sorted([t for t in self.trips if date in t.service])
        return sorted(self.trips)
    
    def get_routes(self, service_group=None, date=None):
        '''Returns all routes from this block'''
        trips = self.get_trips(service_group, date)
        if not trips:
            trips = self.get_trips()
        return sorted({t.route for t in trips})
    
    def get_routes_string(self, service_group=None, date=None):
        '''Returns a string of all routes from this block'''
        return ', '.join([r.number for r in self.get_routes(service_group, date)])
    
    def get_start_time(self, service_group=None, date=None):
        '''Returns the start time of this block'''
        trips = self.get_trips(service_group, date)
        if not trips:
            trips = self.get_trips()
        try:
            return trips[0].start_time
        except IndexError:
            return Time.unknown()
    
    def get_end_time(self, service_group=None, date=None):
        '''Returns the end time of this block'''
        trips = self.get_trips(service_group, date)
        if not trips:
            trips = self.get_trips()
        try:
            return trips[-1].end_time
        except IndexError:
            return Time.unknown()
    
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
        return Match(f'Block {id}', message, 'block', f'blocks/{self.url_id}', value)
