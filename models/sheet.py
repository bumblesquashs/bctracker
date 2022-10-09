
from models.date import Date
from models.service import ServiceGroup

class Sheet:
    '''A collection of overlapping services with defined start and end dates'''
    
    __slots__ = ('system', 'services', 'start_date', 'end_date', '_service_groups')
    
    def __init__(self, service):
        self.system = service.system
        self.services = [service]
        self.start_date = service.start_date
        self.end_date = service.end_date
        
        self._service_groups = None
    
    def __str__(self):
        if self.start_date == self.end_date:
            return str(self.start_date)
        return f'{self.start_date} to {self.end_date}'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return self.services == other.services
    
    def __lt__(self, other):
        return self.start_date < other.start_date
    
    @property
    def service_groups(self):
        '''Returns a list of non-overlapping service groups created from the services associated with this sheet'''
        if self._service_groups is None:
            groups = []
            
            dates = {d for s in self.services for d in s.included_dates if s.special}
            date_services = {d:tuple({s for s in self.services if s.includes(d)}) for d in dates}
            special_service_sets = set(date_services.values())
            for service_set in special_service_sets:
                groups.append(ServiceGroup.combine(self.system, service_set, set()))
            
            weekdays = {w for s in self.services for w in s.weekdays if not s.special}
            weekday_services = {w:tuple({s for s in self.services if w in s.weekdays}) for w in weekdays}
            service_sets = set(weekday_services.values())
            for service_set in service_sets:
                service_set_weekdays = {k for k,v in weekday_services.items() if v == service_set}
                groups.append(ServiceGroup.combine(self.system, service_set, service_set_weekdays))
            self._service_groups = sorted(groups)
        return self._service_groups
    
    @property
    def is_current(self):
        '''Checks if the current date is within this sheet's start and end dates'''
        return self.start_date <= Date.today(self.system.timezone) <= self.end_date
    
    def add_service(self, service):
        '''Adds a service to this sheet'''
        self.services.append(service)
        self.start_date = min(self.start_date, service.start_date)
        self.end_date = max(self.end_date, service.end_date)
        self._service_groups = None
