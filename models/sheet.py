
from models.date import Date
from models.schedule import Schedule

class Sheet:
    '''A collection of overlapping services'''
    
    __slots__ = ('system', 'schedule', 'services', 'service_groups', 'copies')
    
    @classmethod
    def combine(cls, system, services, date_range):
        '''Returns a sheet that includes all of the given services'''
        schedule = Schedule.combine([s.schedule for s in services], date_range)
        return cls(system, schedule, services)
    
    def __init__(self, system, schedule, services):
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
            service_groups.append(service_group)
        
        self.service_groups = sorted(service_groups)
    
    def __str__(self):
        if self.schedule.is_special:
            return self.schedule.added_dates_string
        return str(self.schedule.date_range)
    
    def __hash__(self):
        return hash(self.schedule)
    
    def __eq__(self, other):
        return self.schedule == other.schedule
    
    def __lt__(self, other):
        return self.schedule < other.schedule
    
    @property
    def normal_service_groups(self):
        '''Returns service groups that are not special'''
        service_groups = [g for g in self.service_groups if not g.schedule.is_special]
        if len(service_groups) == 0:
            return self.service_groups
        return service_groups
    
    def copy(self, services):
        '''Returns a duplicate of this sheet, restricted to the given services'''
        services = [s for s in self.services if s in services]
        key = tuple(sorted(services))
        if key in self.copies:
            return self.copies[key]
        if len(services) == 0:
            return None
        copy = Sheet.combine(self.system, services, self.schedule.date_range)
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
