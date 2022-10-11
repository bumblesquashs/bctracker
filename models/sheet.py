
import helpers.date

from models.schedule import Schedule

class Sheet:
    '''A collection of overlapping services'''
    
    __slots__ = ('system', 'id', 'schedule', 'services', 'service_groups')
    
    @classmethod
    def combine(cls, system, services):
        id = '_'.join(sorted({s.id for s in services}))
        service_groups = []
        dates = {d for s in services for d in s.schedule.included_dates if s.schedule.special}
        date_services = {d:tuple({s for s in services if s.schedule.special and s.schedule.includes(d)}) for d in dates}
        special_service_sets = set(date_services.values())
        for service_set in special_service_sets:
            included_dates = {k for k,v in date_services.items() if v == service_set}
            service_groups.append(ServiceGroup.combine(system, service_set, included_dates=included_dates))
        weekdays = {w for s in services for w in s.schedule.weekdays if not s.schedule.special}
        weekday_services = {w:tuple({s for s in services if w in s.schedule.weekdays}) for w in weekdays}
        service_sets = set(weekday_services.values())
        for service_set in service_sets:
            service_set_weekdays = {k for k,v in weekday_services.items() if v == service_set}
            service_groups.append(ServiceGroup.combine(system, service_set, weekdays=service_set_weekdays))
        schedule = Schedule()
        return cls(system, id, schedule, services, sorted(service_groups))
    
    def __init__(self, system, id, schedule, services, service_groups):
        self.system = system
        self.id = id
        self.schedule = schedule
        self.services = services
        self.service_groups = service_groups
    
    def __str__(self):
        return self.schedule.date_string
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.schedule.start_date < other.schedule.start_date

class ServiceGroup:
    '''A collection of services represented as a single schedule'''
    
    __slots__ = ('system', 'id', 'schedule', 'services', 'modified_dates')
    
    @classmethod
    def combine(cls, system, services, weekdays=None, included_dates=None, excluded_dates=None):
        '''Returns a service group that combines a list of services'''
        if len(services) == 0:
            return None
        id = '_'.join(sorted({s.id for s in services}))
        schedules = [s.schedule for s in services]
        start_date = min({s.start_date for s in schedules})
        end_date = max({s.end_date for s in schedules})
        if weekdays is None:
            weekdays = {w for s in schedules for w in s.weekdays}
        if included_dates is None:
            included_dates = {d for s in schedules for d in s.included_dates}
        if excluded_dates is None:
            excluded_dates = {d for s in schedules for d in s.excluded_dates}
        modified_dates = included_dates.intersection(excluded_dates)
        schedule = Schedule(start_date, end_date, weekdays, included_dates - modified_dates, excluded_dates - modified_dates)
        return cls(system, id, schedule, services, modified_dates)
    
    def __init__(self, system, id, schedule, services, modified_dates):
        self.system = system
        self.id = id
        self.schedule = schedule
        self.services = services
        self.modified_dates = modified_dates
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    @property
    def modified_dates_string(self):
        '''Returns a formatted string of dates that are modified in this service group'''
        return helpers.date.flatten(sorted(self.modified_dates))
