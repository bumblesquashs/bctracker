
from datetime import datetime, timedelta

from models.service import ServiceGroup, ServiceSchedule

import formatting

class Sheet:
    __slots__ = ('services', 'start_date', 'end_date', '_service_groups')
    
    def __init__(self, service):
        self.services = [service]
        self.start_date = service.start_date
        self.end_date = service.end_date
        
        self._service_groups = None
    
    def __str__(self):
        start = formatting.long(self.start_date)
        end = formatting.long(self.end_date)
        return f'{start} to {end}'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return self.services == other.services
    
    def __lt__(self, other):
        return self.start_date < other.start_date
    
    @property
    def service_groups(self):
        if self._service_groups is None:
            groups = [ServiceGroup([s], s.schedule) for s in self.services if s.schedule.special]
            services = [s for s in self.services if not s.schedule.special]
            indices = {i for s in services for i in s.schedule.indices}
            index_services = {i:tuple({s for s in services if i in s.schedule.indices}) for i in indices}
            service_sets = set(index_services.values())
            for service_set in service_sets:
                service_set_indices = {k for k,v in index_services.items() if v == service_set}
                mon = 0 in service_set_indices
                tue = 1 in service_set_indices
                wed = 2 in service_set_indices
                thu = 3 in service_set_indices
                fri = 4 in service_set_indices
                sat = 5 in service_set_indices
                sun = 6 in service_set_indices
                schedule = ServiceSchedule(mon, tue, wed, thu, fri, sat, sun)
                groups.append(ServiceGroup(sorted(service_set), schedule))
            self._service_groups = sorted(groups, key=lambda g: g.schedule)
        return self._service_groups
    
    @property
    def is_current(self):
        hour = datetime.now().hour
        today = datetime.today()
        date = (today if hour >= 4 else today - timedelta(days=1)).date()
        return self.start_date <= date <= self.end_date
    
    def add_service(self, service):
        self.services.append(service)
        self.start_date = min(self.start_date, service.start_date)
        self.end_date = max(self.end_date, service.end_date)
        self._service_groups = None

def create_sheets(services):
    sheets = []
    for service in sorted(services, key=lambda s: s.start_date):
        added = False
        for sheet in sheets:
            if service.start_date <= sheet.end_date and service.end_date >= sheet.start_date:
                sheet.add_service(service)
                added = True
        if not added:
            sheets.append(Sheet(service))
    return sorted(sheets)
