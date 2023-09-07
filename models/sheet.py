
from models.date import Date
from models.schedule import Schedule

class Sheet:
    '''A collection of overlapping services'''
    
    __slots__ = ('system', 'schedule', 'services', 'service_groups', 'copies')
    
    @classmethod
    def combine(cls, system, services, date_range, include_special=False):
        '''Returns a sheet that includes all of the given services'''
        schedule = Schedule.combine([s.schedule for s in services], date_range)
        return cls(system, schedule, services, include_special)
    
    def __init__(self, system, schedule, services, include_special=False):
        self.system = system
        self.schedule = schedule
        self.services = services
        self.copies = {}
        
        service_groups = []
        date_services = {d:tuple({s for s in services if d in s.schedule}) for d in schedule.dates}
        for service_set in set(date_services.values()):
            if len(service_set) == 0:
                continue
            dates = {k for k,v in date_services.items() if v == service_set}
            service_group = ServiceGroup(system, dates, schedule.date_range, service_set)
            if include_special or not service_group.schedule.is_special:
                service_groups.append(service_group)
        
        self.service_groups = sorted(service_groups)
    
    def __str__(self):
        return str(self.schedule.date_range)
    
    def __hash__(self):
        return hash(self.schedule)
    
    def __eq__(self, other):
        return self.schedule == other.schedule
    
    def __lt__(self, other):
        return self.schedule < other.schedule
    
    def copy(self, services, include_special=False):
        '''Returns a duplicate of this sheet, restricted to the given services'''
        services = [s for s in self.services if s in services]
        key = (tuple(sorted(services)), include_special)
        if key in self.copies:
            return self.copies[key]
        if len(services) == 0:
            return None
        copy = Sheet.combine(self.system, services, self.schedule.date_range, include_special)
        self.copies[key] = copy
        return copy

class ServiceGroup:
    '''A collection of services represented as a single schedule'''
    
    __slots__ = ('system', 'schedule', 'services')
    
    def __init__(self, system, dates, date_range, services):
        self.system = system
        self.schedule = Schedule(dates, date_range)
        self.services = services
    
    def __str__(self):
        return str(self.schedule)
    
    def __hash__(self):
        return hash(self.schedule)
    
    def __eq__(self, other):
        return self.schedule == other.schedule
    
    def __lt__(self, other):
        return self.schedule < other.schedule
    
    @property
    def is_today(self):
        '''Checks if this service group runs on the current date'''
        return Date.today(self.system.timezone) in self.schedule
