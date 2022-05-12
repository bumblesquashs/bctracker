
from models.service import ServiceGroup
from models.sheet import create_sheets

class Block:
    '''A list of trips that are operated by the same bus sequentially'''
    
    __slots__ = ('system', 'id', 'trips', 'service_group', 'sheets')
    
    def __init__(self, system, id, trips):
        self.system = system
        self.id = id
        self.trips = sorted(trips)
        
        services = {t.service for t in trips}
        self.service_group = ServiceGroup.combine(services)
        self.sheets = create_sheets(services)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    @property
    def today_service_group(self):
        for sheet in self.sheets:
            for service_group in sheet.service_groups:
                if service_group.is_today:
                    return service_group
        return None
    
    @property
    def related_blocks(self):
        related_blocks = [b for b in self.system.get_blocks() if self.is_related(b)]
        return sorted(related_blocks, key=lambda b: b.service_group)
    
    def get_trips(self, service_group=None):
        if service_group is None:
            return self.trips
        return [t for t in self.trips if t.service in service_group.services]
    
    def get_routes(self, service_group=None):
        return sorted({t.route for t in self.get_trips(service_group)})
    
    def get_routes_string(self, service_group=None):
        return ', '.join([r.number for r in self.get_routes(service_group)])
    
    def get_start_time(self, service_group=None):
        trips = self.get_trips(service_group)
        if len(trips) == 0:
            return None
        return trips[0].start_time
    
    def get_end_time(self, service_group=None):
        trips = self.get_trips(service_group)
        if len(trips) == 0:
            return None
        return trips[-1].end_time
    
    def get_duration(self, service_group=None):
        start_time = self.get_start_time(service_group)
        end_time = self.get_end_time(service_group)
        if start_time is None or end_time is None:
            return None
        return start_time.format_difference(end_time)
    
    def is_related(self, other):
        if self.id == other.id:
            return False
        if self.get_routes() != other.get_routes():
            return False
        if self.get_start_time() != other.get_start_time():
            return False
        if self.get_end_time() != other.get_end_time():
            return False
        return True
