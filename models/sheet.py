
from models.date import Date
from models.daterange import DateRange
from models.schedule import Schedule

class Sheet:
    '''A collection of overlapping services'''
    
    __slots__ = ('system', 'id', 'schedule', 'services', 'service_groups')
    
    @classmethod
    def combine(cls, system, services, include_special):
        '''Returns a sheet that includes all of the given services'''
        id = '_'.join(sorted({s.id for s in services}))
        schedule = Schedule.combine([s.schedule for s in services])
        service_groups = []
        weekdays = {w for s in services for w in s.schedule.weekdays if not s.schedule.special}
        weekday_services = {w:tuple({s for s in services if w in s.schedule.weekdays}) for w in weekdays}
        for service_set in set(weekday_services.values()):
            service_set_weekdays = {k for k,v in weekday_services.items() if v == service_set}
            service_groups.append(ServiceGroup.combine(system, service_set, weekdays=service_set_weekdays))
        if include_special or len(service_groups) == 0:
            dates = {d for s in services for d in s.schedule.modified_dates if s.schedule.special}
            date_services = {d:tuple({s for s in services if s.schedule.includes(d)}) for d in dates}
            for service_set in set(date_services.values()):
                modified_dates = {k for k,v in date_services.items() if v == service_set}
                service_groups.append(ServiceGroup.combine(system, service_set, weekdays=set(), modified_dates=modified_dates))
        return cls(system, id, schedule, services, sorted(service_groups))
    
    def __init__(self, system, id, schedule, services, service_groups):
        self.system = system
        self.id = id
        self.schedule = schedule
        self.services = services
        self.service_groups = service_groups
    
    def __str__(self):
        return str(self.schedule.date_range)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.schedule.date_range < other.schedule.date_range

class ServiceGroup:
    '''A collection of services represented as a single schedule'''
    
    __slots__ = ('system', 'id', 'schedule', 'services')
    
    @classmethod
    def combine(cls, system, services, weekdays=None, modified_dates=None, excluded_dates=None):
        '''Returns a service group that combines a list of services'''
        if len(services) == 0:
            return None
        id = '_'.join(sorted({s.id for s in services}))
        schedules = [s.schedule for s in services]
        date_range = DateRange.combine([s.date_range for s in schedules])
        if weekdays is None:
            weekdays = {w for s in schedules for w in s.weekdays}
        if modified_dates is None:
            modified_dates = {d for s in schedules for d in s.modified_dates}
        if excluded_dates is None:
            excluded_dates = {d for s in schedules for d in s.excluded_dates}
        for date in excluded_dates:
            if len([s for s in schedules if date in s.excluded_dates]) < len([s for s in schedules if date.weekday in s.weekdays]):
                modified_dates.add(date)
        schedule = Schedule(date_range, weekdays, modified_dates, excluded_dates - modified_dates)
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
        '''Returns whether or not this service group runs on the current date'''
        return self.schedule.includes(Date.today(self.system.timezone))
