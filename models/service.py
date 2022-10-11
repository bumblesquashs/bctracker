
from enum import IntEnum

import helpers.date

from models.date import Date
from models.schedule import Schedule
from models.weekday import Weekday

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

class Service:
    '''A schedule with an ID'''
    
    __slots__ = ('system', 'id', 'schedule')
    
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
        
        weekdays = {Weekday(i) for i, v in enumerate([mon, tue, wed, thu, fri, sat, sun]) if v}
        service_exceptions = exceptions.get(id, [])
        included_dates = {e.date for e in service_exceptions if e.type == ServiceExceptionType.INCLUDED}
        excluded_dates = {e.date for e in service_exceptions if e.type == ServiceExceptionType.EXCLUDED}
        schedule = Schedule.process(start_date, end_date, weekdays, included_dates, excluded_dates)
        return cls(system, id, schedule)
    
    def __init__(self, system, id, schedule):
        self.system = system
        self.id = id
        self.schedule = schedule
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
