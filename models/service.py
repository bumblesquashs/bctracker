
from datetime import timedelta
from enum import IntEnum

import helpers.date

from models.date import Date, Weekday

class ServiceExceptionType(IntEnum):
    INCLUDED = 1
    EXCLUDED = 2

class ServiceException:
    '''A date that is explicitly included or excluded from a service'''
    
    __slots__ = ('service_id', 'date', 'type')
    
    @classmethod
    def from_csv(cls, row, system):
        '''Returns a service exception initialized from the given CSV row'''
        service_id = row['service_id']
        date = Date.parse_csv(row['date'], system.timezone)
        type = ServiceExceptionType(int(row['exception_type']))
        return cls(service_id, date, type)
    
    def __init__(self, service_id, date, type):
        self.service_id = service_id
        self.date = date
        self.type = type
    
    def __hash__(self):
        return hash((self.service_id, self.date))
    
    def __eq__(self, other):
        return self.service_id == other.service_id and self.date == other.date

class ServicePattern:
    '''The days of a week when a service is or is not running within a given date range'''
    
    __slots__ = ('system', 'id', 'start_date', 'end_date', 'weekdays', 'included_dates', 'excluded_dates', 'special', 'avg_days', 'binary_string', 'name')
    
    def __init__(self, system, id, start_date, end_date, weekdays, included_dates, excluded_dates):
        for weekday in Weekday:
            if weekday in weekdays:
                explicit_dates = {d for d in excluded_dates if d.weekday == weekday}
            else:
                explicit_dates = {d for d in included_dates if d.weekday == weekday}
            implicit_dates = get_implicit_dates(weekday, start_date, end_date, explicit_dates)
            if len(explicit_dates) == 0 and len(implicit_dates) == 0:
                if weekday in weekdays:
                    weekdays.remove(weekday)
            elif len(explicit_dates) > len(implicit_dates):
                if weekday in weekdays:
                    weekdays.remove(weekday)
                    included_dates = included_dates.union(implicit_dates)
                    excluded_dates -= explicit_dates
                else:
                    weekdays.add(weekday)
                    included_dates -= explicit_dates
                    excluded_dates = excluded_dates.union(implicit_dates)
        
        self.system = system
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.weekdays = weekdays
        self.included_dates = included_dates
        self.excluded_dates = excluded_dates
        
        self.special = len(weekdays) == 0
        self.avg_days = ((end_date.datetime - start_date.datetime).days + 1) / 7
        self.binary_string = ''.join(['1' if d in weekdays else '0' for d in sorted(Weekday)])
        
        if self.special:
            self.name = 'Special Service'
        elif weekdays == {Weekday.MON, Weekday.TUE, Weekday.WED, Weekday.THU, Weekday.FRI, Weekday.SAT, Weekday.SUN}:
            self.name = 'Every Day'
        elif weekdays == {Weekday.MON, Weekday.TUE, Weekday.WED, Weekday.THU, Weekday.FRI}:
            self.name = 'Weekdays'
        elif weekdays == {Weekday.MON}:
            self.name = 'Mondays'
        elif weekdays == {Weekday.TUE}:
            self.name = 'Tuesdays'
        elif weekdays == {Weekday.WED}:
            self.name = 'Wednesdays'
        elif weekdays == {Weekday.THU}:
            self.name = 'Thursdays'
        elif weekdays == {Weekday.FRI}:
            self.name = 'Fridays'
        elif weekdays == {Weekday.SAT, Weekday.SUN}:
            self.name = 'Weekends'
        elif weekdays == {Weekday.SAT}:
            self.name = 'Saturdays'
        elif weekdays == {Weekday.SUN}:
            self.name = 'Sundays'
        else:
            self.name = '/'.join([str(d) for d in sorted(weekdays)])
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if self.special and other.special:
            if len(self.included_dates) > 0 and len(other.included_dates) > 0:
                return self.included_dates == other.included_dates
            return self.start_date == other.start_date and self.end_date == other.end_date
        return self.binary_string == other.binary_string
    
    def __lt__(self, other):
        if self.special and other.special:
            if len(self.included_dates) > 0 and len(other.included_dates) > 0:
                return sorted(self.included_dates)[0] < sorted(other.included_dates)[0]
            return self.start_date < other.start_date
        return self.binary_string > other.binary_string
    
    @property
    def included_dates_string(self):
        '''Returns a formatted string of service exception dates that are included in this service pattern'''
        return helpers.date.flatten(sorted(self.included_dates))
    
    @property
    def excluded_dates_string(self):
        '''Returns a formatted string of service exception dates that are excluded from this service pattern'''
        return helpers.date.flatten(sorted(self.excluded_dates))
    
    @property
    def date_string(self):
        '''Returns a string indicating the date/dates/date range that this service pattern operates'''
        if self.special and len(self.included_dates) > 0:
            return self.included_dates_string
        if self.start_date == self.end_date:
            return str(self.start_date)
        return f'{self.start_date} to {self.end_date}'
    
    @property
    def is_current(self):
        '''Checks if the current date is within this service pattern's start and end dates'''
        return self.start_date <= Date.today(self.system.timezone) <= self.end_date
    
    @property
    def is_today(self):
        '''Checks if this service pattern includes the current date'''
        return self.includes(Date.today(self.system.timezone))
    
    def includes(self, date):
        '''Checks if this service pattern includes the given date'''
        if date < self.start_date or date > self.end_date:
            return False
        if date in self.included_dates:
            return True
        if date in self.excluded_dates:
            return False
        return date.weekday in self.weekdays
    
    def get_status(self, weekday):
        '''Returns the status class of this service on the given weekday'''
        if weekday in self.weekdays:
            return 'running'
        if len([d for d in self.included_dates if d.weekday == weekday]) > 0:
            return 'limited'
        return 'not-running'

class Service(ServicePattern):
    '''A predefined service pattern'''
    
    @classmethod
    def from_csv(cls, row, system, exceptions):
        '''Returns a service initialized from the given CSV row'''
        id = row['service_id']
        start_date = Date.parse_csv(row['start_date'], system.timezone)
        end_date = Date.parse_csv(row['end_date'], system.timezone)
        mon = row['monday'] == '1'
        tue = row['tuesday'] == '1'
        wed = row['wednesday'] == '1'
        thu = row['thursday'] == '1'
        fri = row['friday'] == '1'
        sat = row['saturday'] == '1'
        sun = row['sunday'] == '1'
        
        values = [mon, tue, wed, thu, fri, sat, sun]
        weekdays = {Weekday(i) for i, v in enumerate(values) if v}
        service_exceptions = exceptions.get(id, [])
        included_dates = {e.date for e in service_exceptions if e.type == ServiceExceptionType.INCLUDED}
        excluded_dates = {e.date for e in service_exceptions if e.type == ServiceExceptionType.EXCLUDED}
        return cls(system, id, start_date, end_date, weekdays, included_dates, excluded_dates)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    @property
    def sheet(self):
        '''Returns the sheet associated with this service'''
        return self.system.get_sheet(self.id)

class ServiceGroup(ServicePattern):
    '''A collection of services represented as a single service pattern'''
    
    __slots__ = ('services', 'modified_dates')
    
    @classmethod
    def combine(cls, system, services):
        '''Returns a service group that combines a list of services'''
        if len(services) == 0:
            return None
        id = '_'.join(sorted({s.id for s in services}))
        start_date = min({s.start_date for s in services})
        end_date = max({s.end_date for s in services})
        weekdays = {d for s in services for d in s.weekdays}
        included_dates = {d for s in services for d in s.included_dates}
        excluded_dates = {d for s in services for d in s.excluded_dates}
        return cls(system, id, start_date, end_date, weekdays, included_dates, excluded_dates, services)
    
    def __init__(self, system, id, start_date, end_date, weekdays, included_dates, excluded_dates, services):
        modified_dates = included_dates.intersection(excluded_dates)
        super().__init__(system, id, start_date, end_date, weekdays, included_dates - modified_dates, excluded_dates - modified_dates)
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

def get_implicit_dates(weekday, start_date, end_date, explicit_dates):
    implicit_dates = set()
    date = start_date
    while date.weekday != weekday:
        date += timedelta(days=1)
    while date <= end_date:
        if date not in explicit_dates:
            implicit_dates.add(date)
        date += timedelta(weeks=1)
    return implicit_dates
