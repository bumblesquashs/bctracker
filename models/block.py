
import helpers.sheet

from models.schedule import Schedule

class Block:
    '''A list of trips that are operated by the same bus sequentially'''
    
    __slots__ = ('system', 'id', 'trips', 'schedule', 'sheets')
    
    def __init__(self, system, id, trips):
        self.system = system
        self.id = id
        self.trips = trips
        
        services = {t.service for t in trips}
        self.schedule = Schedule.combine([s.schedule for s in services])
        self.sheets = helpers.sheet.combine(system, services, True)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    @property
    def today_service_group(self):
        '''Returns the service group from this block running on the current date, or None'''
        for sheet in self.sheets:
            for service_group in sheet.service_groups:
                if service_group.is_today:
                    return service_group
        return None
    
    @property
    def related_blocks(self):
        '''Returns all blocks that have the same start time, end time, and routes as this block'''
        related_blocks = [b for b in self.system.get_blocks() if self.is_related(b)]
        return sorted(related_blocks, key=lambda b: b.schedule)
    
    def get_trips(self, service_group=None):
        '''Returns all trips from this block that are part of the given service group'''
        if service_group is None:
            return sorted(self.trips)
        return sorted([t for t in self.trips if t.service in service_group.services])
    
    def get_routes(self, service_group=None):
        '''Returns all routes from this block that are part of the given service group'''
        return sorted({t.route for t in self.get_trips(service_group)})
    
    def get_routes_string(self, service_group=None):
        '''Returns a string of all routes from this block that are part of the given service group'''
        return ', '.join([r.number for r in self.get_routes(service_group)])
    
    def get_start_time(self, service_group=None):
        '''Returns the start time of this block based on the given service group'''
        trips = self.get_trips(service_group)
        if len(trips) == 0:
            return None
        return trips[0].start_time
    
    def get_end_time(self, service_group=None):
        '''Returns the end time of this block based on the given service group'''
        trips = self.get_trips(service_group)
        if len(trips) == 0:
            return None
        return trips[-1].end_time
    
    def get_duration(self, service_group=None):
        '''Returns the duration of this block based on the given service group'''
        start_time = self.get_start_time(service_group)
        end_time = self.get_end_time(service_group)
        if start_time is None or end_time is None:
            return None
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
