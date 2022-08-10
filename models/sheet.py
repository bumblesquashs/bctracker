
from models.date import Date
from models.service import ServiceGroup, ServiceException, ServiceExceptionType

class Sheet:
    '''A collection of overlapping services with defined start and end dates'''
    
    __slots__ = ('services', 'start_date', 'end_date', '_service_groups')
    
    def __init__(self, service):
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
                id = '_'.join(sorted([s.id for s in service_set]))
                start_date = min({s.start_date for s in service_set})
                end_date = max({s.end_date for s in service_set})
                service_set_dates = {k for k,v in date_services.items() if v == service_set}
                exceptions = [ServiceException(id, d, ServiceExceptionType.INCLUDED) for d in service_set_dates]
                groups.append(ServiceGroup(id, sorted(service_set), start_date, end_date, False, False, False, False, False, False, False, exceptions))
            
            indices = {i for s in self.services for i in s.indices if not s.special}
            index_services = {i:tuple({s for s in self.services if i in s.indices}) for i in indices}
            service_sets = set(index_services.values())
            for service_set in service_sets:
                id = '_'.join(sorted([s.id for s in service_set]))
                start_date = min({s.start_date for s in service_set})
                end_date = max({s.end_date for s in service_set})
                service_set_indices = {k for k,v in index_services.items() if v == service_set}
                mon = 0 in service_set_indices
                tue = 1 in service_set_indices
                wed = 2 in service_set_indices
                thu = 3 in service_set_indices
                fri = 4 in service_set_indices
                sat = 5 in service_set_indices
                sun = 6 in service_set_indices
                exceptions = {e for s in service_set for e in s.exceptions}
                groups.append(ServiceGroup(id, sorted(service_set), start_date, end_date, mon, tue, wed, thu, fri, sat, sun, exceptions))
            self._service_groups = sorted(groups)
        return self._service_groups
    
    @property
    def is_current(self):
        '''Checks if the current date is within this sheet's start and end dates'''
        return self.start_date <= Date.today() <= self.end_date
    
    def add_service(self, service):
        '''Adds a service to this sheet'''
        self.services.append(service)
        self.start_date = min(self.start_date, service.start_date)
        self.end_date = max(self.end_date, service.end_date)
        self._service_groups = None
