
from models.date import Date
from models.schedule import Schedule

class Sheet:
    '''A collection of overlapping services'''
    
    __slots__ = ('system', 'schedule', 'services', 'service_groups', 'copies')
    
    @classmethod
    def combine(cls, system, services, include_special=False):
        '''Returns a sheet that includes all of the given services'''
        services = {s for s in services if not s.schedule.is_empty}
        schedule = Schedule.combine([s.schedule for s in services])
        return cls(system, schedule, services, include_special)
    
    def __init__(self, system, schedule, services, include_special=False):
        self.system = system
        self.schedule = schedule
        self.services = services
        self.copies = {}
        
        service_groups = []
        weekday_services = {w:tuple({s for s in services if w in s.schedule.weekdays}) for w in schedule.weekdays}
        for service_set in set(weekday_services.values()):
            service_set_weekdays = {k for k,v in weekday_services.items() if v == service_set}
            service_groups.append(ServiceGroup.combine(self.system, service_set, date_range=self.schedule.date_range, weekdays=service_set_weekdays))
        if include_special or len(service_groups) == 0:
            date_services = {d:tuple({s for s in services if d in s.schedule}) for d in schedule.added_dates}
            for service_set in set(date_services.values()):
                if service_set in weekday_services.values():
                    continue
                exceptions = {k for k,v in date_services.items() if v == service_set}
                service_groups.append(ServiceGroup.combine(self.system, service_set, date_range=self.schedule.date_range, weekdays=set(), exceptions=exceptions))
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
    
    def copy(self, services, include_special=False):
        '''Returns a duplicate of this sheet, restricted to the given services'''
        services = [s for s in self.services if s in services]
        key = (tuple(sorted(services)), include_special)
        if key in self.copies:
            return self.copies[key]
        if len(services) == 0:
            return None
        copy = Sheet.combine(self.system, services, include_special)
        self.copies[key] = copy
        return copy

class ServiceGroup:
    '''A collection of services represented as a single schedule'''
    
    __slots__ = ('system', 'schedule', 'services', 'name')
    
    @classmethod
    def combine(cls, system, services, date_range=None, weekdays=None, exceptions=None, modifications=None):
        '''Returns a service group that combines a list of services'''
        if len(services) == 0:
            return None
        schedules = [s.schedule for s in services]
        schedule = Schedule.combine(schedules, date_range, weekdays, exceptions, modifications)
        return cls(system, schedule, services)
    
    def __init__(self, system, schedule, services):
        self.system = system
        self.schedule = schedule
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
