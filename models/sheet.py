
from models.date import Date
from models.schedule import Schedule

class Sheet:
    '''A collection of overlapping services'''
    
    __slots__ = ('system', 'id', 'schedule', 'services')
    
    @classmethod
    def combine(cls, system, services):
        '''Returns a sheet that includes all of the given services'''
        services = {s for s in services if not s.schedule.is_empty}
        id = '_'.join(sorted({s.id for s in services}))
        schedule = Schedule.combine([s.schedule for s in services])
        return cls(system, id, schedule, services)
    
    def __init__(self, system, id, schedule, services):
        self.system = system
        self.id = id
        self.schedule = schedule
        self.services = services
    
    def __str__(self):
        if self.schedule.is_special:
            return self.schedule.added_dates_string
        return str(self.schedule.date_range)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.schedule < other.schedule
    
    def __contains__(self, services):
        return not self.services.isdisjoint(services)
    
    def get_schedule(self, services=None):
        '''Returns the schedule for this sheet'''
        if services is None:
            services = self.services
        else:
            services = [s for s in services if s in self.services]
        return Schedule.combine([s.schedule for s in services], self.schedule.date_range)
    
    def get_service_groups(self, services=None, include_special=False):
        '''Returns the service groups for this sheet'''
        if services is None:
            services = self.services
        else:
            services = [s for s in services if s in self.services]
        service_groups = []
        weekdays = {w for s in services for w in s.schedule.weekdays if not s.schedule.is_special}
        weekday_services = {w:tuple({s for s in services if w in s.schedule.weekdays}) for w in weekdays}
        for service_set in set(weekday_services.values()):
            service_set_weekdays = {k for k,v in weekday_services.items() if v == service_set}
            service_groups.append(ServiceGroup.combine(self.system, service_set, date_range=self.schedule.date_range, weekdays=service_set_weekdays))
        if include_special or len(service_groups) == 0:
            dates = {d for s in services for d in s.schedule.added_dates if s.schedule.is_special}
            date_services = {d:tuple({s for s in services if d in s.schedule}) for d in dates}
            for service_set in set(date_services.values()):
                exceptions = {k for k,v in date_services.items() if v == service_set}
                service_groups.append(ServiceGroup.combine(self.system, service_set, date_range=self.schedule.date_range, weekdays=set(), exceptions=exceptions))
        return sorted(service_groups)

class ServiceGroup:
    '''A collection of services represented as a single schedule'''
    
    __slots__ = ('system', 'id', 'schedule', 'services', 'name')
    
    @classmethod
    def combine(cls, system, services, date_range=None, weekdays=None, exceptions=None, modifications=None):
        '''Returns a service group that combines a list of services'''
        if len(services) == 0:
            return None
        id = '_'.join(sorted({s.id for s in services}))
        schedules = [s.schedule for s in services]
        schedule = Schedule.combine(schedules, date_range, weekdays, exceptions, modifications)
        return cls(system, id, schedule, services)
    
    def __init__(self, system, id, schedule, services):
        self.system = system
        self.id = id
        self.schedule = schedule
        self.services = services
    
    def __str__(self):
        return str(self.schedule)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.schedule < other.schedule
    
    @property
    def is_today(self):
        '''Checks if this service group runs on the current date'''
        return Date.today(self.system.timezone) in self.schedule
