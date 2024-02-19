
from models.schedule import Schedule

class Sheet:
    '''A collection of overlapping services'''
    
    __slots__ = (
        'system',
        'agency',
        'schedule',
        'services',
        'service_groups',
        'modifications',
        'copies'
    )
    
    @property
    def normal_service_groups(self):
        '''Returns service groups that are not special'''
        service_groups = [g for g in self.service_groups if not g.schedule.is_special]
        if len(service_groups) == 0:
            return self.service_groups
        return service_groups
    
    @property
    def has_normal_service(self):
        '''Checks if this sheet indicates normal service'''
        return self.schedule.has_normal_service
    
    @property
    def has_modified_service(self):
        '''Checks if this sheet indicates modified service'''
        return len(self.modifications) > 0
    
    @property
    def has_no_service(self):
        '''Checks if this sheet indicates no service'''
        return self.schedule.has_no_service
    
    def __init__(self, system, agency, services, date_range):
        self.system = system
        self.agency = agency
        self.schedule = Schedule.combine(services, date_range)
        self.services = services
        self.copies = {}
        
        service_groups = []
        date_services = {d:tuple({s for s in services if d in s}) for d in self.schedule.dates}
        for service_set in set(date_services.values()):
            if len(service_set) == 0:
                continue
            dates = {k for k,v in date_services.items() if v == service_set}
            service_group = ServiceGroup(system, agency, dates, date_range, service_set)
            service_groups.append(service_group)
        
        self.service_groups = sorted(service_groups)
        
        added_dates = {d for g in service_groups for d in g.schedule.added_dates}
        removed_dates = {d for g in service_groups for d in g.schedule.removed_dates}
        self.modifications = added_dates.intersection(removed_dates)
    
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
    
    def copy(self, services):
        '''Returns a duplicate of this sheet, restricted to the given services'''
        services = [s for s in self.services if s in services]
        key = tuple(sorted(services))
        if key in self.copies:
            return self.copies[key]
        if len(services) == 0:
            return None
        copy = Sheet(self.system, services, self.schedule.date_range)
        self.copies[key] = copy
        return copy
    
    def get_weekday_status(self, weekday):
        '''Returns the status class of this schedule on the given weekday'''
        return self.schedule.get_weekday_status(weekday)
    
    def get_date_status(self, date):
        '''Returns the status class of this schedule on the given date'''
        if date in self.modifications:
            return 'modified-service'
        return self.schedule.get_date_status(date)

class ServiceGroup:
    '''A collection of services represented as a single schedule'''
    
    __slots__ = (
        'system',
        'agency',
        'schedule',
        'services'
    )
    
    def __init__(self, system, agency, dates, date_range, services):
        self.system = system
        self.agency = agency
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
    
    def __contains__(self, service):
        return service in self.services
