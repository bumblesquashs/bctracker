
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass
from enum import IntEnum

from models.context import Context
from models.date import Date
from models.daterange import DateRange
from models.schedule import Schedule
from models.weekday import Weekday

class ServiceExceptionType(IntEnum):
    INCLUDED = 1
    EXCLUDED = 2

@dataclass(slots=True)
class ServiceException:
    '''A date that is explicitly included or excluded from a service'''
    
    service_id: str
    date: Date
    type: ServiceExceptionType
    
    @classmethod
    def from_csv(cls, row, context: Context):
        '''Returns a service exception initialized from the given CSV row'''
        service_id = row['service_id']
        date = Date.parse(row['date'], context.timezone, '%Y%m%d')
        type = ServiceExceptionType(int(row['exception_type']))
        return cls(service_id, date, type)
    
    def __hash__(self):
        return hash((self.service_id, self.date))
    
    def __eq__(self, other):
        return self.service_id == other.service_id and self.date == other.date

@dataclass(slots=True)
class Service:
    '''A set of dates when a transit service is operating'''
    
    system: System
    id: int
    schedule: Schedule
    
    @classmethod
    def from_csv(cls, row, context: Context, exceptions, feed_date_range):
        '''Returns a service initialized from the given CSV row'''
        id = row['service_id']
        start_date = Date.parse(row['start_date'], context.timezone, '%Y%m%d')
        end_date = Date.parse(row['end_date'], context.timezone, '%Y%m%d')
        date_range = DateRange(start_date, end_date)
        mon = row['monday'] == '1'
        tue = row['tuesday'] == '1'
        wed = row['wednesday'] == '1'
        thu = row['thursday'] == '1'
        fri = row['friday'] == '1'
        sat = row['saturday'] == '1'
        sun = row['sunday'] == '1'
        
        weekdays = {Weekday(i) for i, v in enumerate([mon, tue, wed, thu, fri, sat, sun]) if v}
        service_exceptions = {e for e in exceptions.get(id, [])}
        added_dates = {e.date for e in service_exceptions if e.type == ServiceExceptionType.INCLUDED}
        removed_dates = {e.date for e in service_exceptions if e.type == ServiceExceptionType.EXCLUDED}
        
        if feed_date_range:
            if feed_date_range.start > date_range.start:
                date_range.start = feed_date_range.start
            if feed_date_range.end < date_range.end:
                date_range.end = feed_date_range.end
        
        dates = {d for d in date_range if d.weekday in weekdays}
        dates.update(added_dates)
        dates.difference_update(removed_dates)
        
        schedule = Schedule(dates, date_range)
        return cls(context.system, id, schedule)
    
    @classmethod
    def combine(cls, context: Context, id, exceptions):
        '''Returns a service based on a list of service exceptions'''
        dates = {e.date for e in exceptions if e.type == ServiceExceptionType.INCLUDED}
        date_range = DateRange(min(dates), max(dates))
        schedule = Schedule(dates, date_range)
        return cls(context.system, id, schedule)
    
    @property
    def context(self):
        '''The context for this service'''
        return self.system.context
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.schedule < other.schedule
    
    def __contains__(self, date):
        return date in self.schedule
