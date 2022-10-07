
from datetime import timedelta
from enum import IntEnum

import helpers.date

from models.date import Date

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
    
    __slots__ = ('start_date', 'end_date', 'timezone', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'exceptions', 'special', 'avg_days', 'indices', 'binary_string', 'name')
    
    def __init__(self, start_date, end_date, timezone, mon, tue, wed, thu, fri, sat, sun, exceptions):
        self.start_date = start_date
        self.end_date = end_date
        self.timezone = timezone
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun
        self.exceptions = exceptions
        
        self.special = not (mon or tue or wed or thu or fri or sat or sun)
        
        self.avg_days = ((end_date.datetime - start_date.datetime).days + 1) / 7
        
        values = [mon, tue, wed, thu, fri, sat, sun]
        self.indices = [i for i, value in enumerate(values) if value]
        self.binary_string = ''.join(['1' if d else '0' for d in values])
        
        if self.special:
            self.name = 'Special Service'
        elif mon and tue and wed and thu and fri and sat and sun:
            self.name = 'Every Day'
        elif mon and tue and wed and thu and fri and not (sat or sun):
            self.name = 'Weekdays'
        elif mon and not (tue or wed or thu or fri or sat or sun):
            self.name = 'Mondays'
        elif tue and not (mon or wed or thu or fri or sat or sun):
            self.name = 'Tuesdays'
        elif wed and not (mon or tue or thu or fri or sat or sun):
            self.name = 'Wednesdays'
        elif thu and not (mon or tue or wed or fri or sat or sun):
            self.name = 'Thursdays'
        elif fri and not (mon or tue or wed or thu or sat or sun):
            self.name = 'Fridays'
        elif sat and sun and not (mon or tue or wed or thu or fri):
            self.name = 'Weekends'
        elif sat and not (mon or tue or wed or thu or fri or sun):
            self.name = 'Saturdays'
        elif sun and not (mon or tue or wed or thu or fri or sat):
            self.name = 'Sundays'
        else:
            days = []
            if mon:
                days.append('Mon')
            if tue:
                days.append('Tue')
            if wed:
                days.append('Wed')
            if thu:
                days.append('Thu')
            if fri:
                days.append('Fri')
            if sat:
                days.append('Sat')
            if sun:
                days.append('Sun')
            self.name = '/'.join(days)
    
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
                return self.included_dates[0] < other.included_dates[0]
            return self.start_date < other.start_date
        return self.binary_string > other.binary_string
    
    @property
    def mon_status(self):
        '''Returns the status class of this service pattern on Mondays'''
        return self.get_status(self.mon, 0)
    
    @property
    def tue_status(self):
        '''Returns the status class of this service pattern on Tuesdays'''
        return self.get_status(self.tue, 1)
    
    @property
    def wed_status(self):
        '''Returns the status class of this service pattern on Wednesdays'''
        return self.get_status(self.wed, 2)
    
    @property
    def thu_status(self):
        '''Returns the status class of this service pattern on Thursdays'''
        return self.get_status(self.thu, 3)
    
    @property
    def fri_status(self):
        '''Returns the status class of this service pattern on Fridays'''
        return self.get_status(self.fri, 4)
    
    @property
    def sat_status(self):
        '''Returns the status class of this service pattern on Saturdays'''
        return self.get_status(self.sat, 5)
    
    @property
    def sun_status(self):
        '''Returns the status class of this service pattern on Sundays'''
        return self.get_status(self.sun, 6)
    
    @property
    def included_dates(self):
        '''Returns service exception dates that are included in this service pattern'''
        included_dates = {e.date for e in self.exceptions if e.type == ServiceExceptionType.INCLUDED}
        excluded_dates = {e.date for e in self.exceptions if e.type == ServiceExceptionType.EXCLUDED}
        return sorted(included_dates - excluded_dates)
    
    @property
    def included_dates_string(self):
        '''Returns a formatted string of service exception dates that are included in this service pattern'''
        return helpers.date.flatten(self.included_dates)
    
    @property
    def excluded_dates(self):
        '''Returns service exception dates that are excluded from this service pattern'''
        excluded_dates = {e.date for e in self.exceptions if e.type == ServiceExceptionType.EXCLUDED}
        included_dates = {e.date for e in self.exceptions if e.type == ServiceExceptionType.INCLUDED}
        return sorted(excluded_dates - included_dates)
    
    @property
    def excluded_dates_string(self):
        '''Returns a formatted string of service exception dates that are excluded from this service pattern'''
        return helpers.date.flatten(self.excluded_dates)
    
    @property
    def date_string(self):
        '''Returns a string indicating the date/dates/date range that this service pattern operates'''
        if len(self.indices) == 0 and len(self.included_dates) > 0:
            return self.included_dates_string
        if self.start_date == self.end_date:
            return str(self.start_date)
        return f'{self.start_date} to {self.end_date}'
    
    @property
    def is_current(self):
        '''Checks if the current date is within this service pattern's start and end dates'''
        return self.start_date <= Date.today(self.timezone) <= self.end_date
    
    @property
    def is_today(self):
        '''Checks if this service pattern includes the current date'''
        return self.includes(Date.today(self.timezone))
    
    def includes(self, date):
        '''Checks if this service pattern includes the given date'''
        if date < self.start_date or date > self.end_date:
            return False
        if date in self.included_dates:
            return True
        if date in self.excluded_dates:
            return False
        return date.weekday in self.indices
    
    def get_status(self, active, weekday):
        '''Returns the status class of this service on the given weekday'''
        included_count = len([d for d in self.included_dates if d.weekday == weekday])
        excluded_count = len([d for d in self.excluded_dates if d.weekday == weekday])
        if active or (included_count / self.avg_days) > 0.3:
            if (excluded_count / self.avg_days) > 0.7:
                return 'limited'
            return 'running'
        if included_count > 0:
            return 'limited'
        return 'not-running'

class Service(ServicePattern):
    '''A service pattern with an id'''
    
    __slots__ = ('system', 'id')
    
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
        
        service_exceptions = exceptions.get(id, [])
        delta = end_date.datetime - start_date.datetime
        if mon and tue and wed and thu and fri and sat and sun and delta.days < 7:
            service_exceptions += [ServiceException(id, start_date + timedelta(days=i), ServiceExceptionType.INCLUDED) for i in range(delta.days + 1)]
            mon = tue = wed = thu = fri = sat = sun = False
        return cls(system, id, start_date, end_date, mon, tue, wed, thu, fri, sat, sun, service_exceptions)
    
    def __init__(self, system, id, start_date, end_date, mon, tue, wed, thu, fri, sat, sun, exceptions):
        super().__init__(start_date, end_date, system.timezone, mon, tue, wed, thu, fri, sat, sun, exceptions)
        self.system = system
        self.id = id
    
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
    
    __slots__ = ('id', 'services')
    
    @classmethod
    def combine(cls, services):
        '''Returns a service group initialized by combined a list of services'''
        if len(services) == 0:
            return None
        id = '_'.join(sorted({s.id for s in services}))
        start_date = min({s.start_date for s in services})
        end_date = max({s.end_date for s in services})
        indices = {i for s in services for i in s.indices}
        mon = 0 in indices
        tue = 1 in indices
        wed = 2 in indices
        thu = 3 in indices
        fri = 4 in indices
        sat = 5 in indices
        sun = 6 in indices
        exceptions = [e for s in services for e in s.exceptions]
        return cls(id, services, start_date, end_date, mon, tue, wed, thu, fri, sat, sun, exceptions)
    
    def __init__(self, id, services, start_date, end_date, mon, tue, wed, thu, fri, sat, sun, exceptions):
        super().__init__(start_date, end_date, list(services)[0].timezone, mon, tue, wed, thu, fri, sat, sun, exceptions)
        self.id = id
        self.services = services
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
