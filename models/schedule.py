
from dataclasses import dataclass, field

from models.date import Date
from models.daterange import DateRange
from models.weekday import Weekday

import helpers

@dataclass(slots=True)
class Schedule:
    '''Dates when a service is running'''
    
    dates: set[Date]
    date_range: DateRange
    
    weekdays: set[Weekday] = field(default_factory=set, init=False)
    exceptions: set[Date] = field(default_factory=set, init=False)
    name: str = field(init=False)
    
    @classmethod
    def combine(cls, services, date_range=None):
        '''Returns a schedule that combines multiple services'''
        if not services:
            return None
        if not date_range:
            date_range = DateRange.combine([s.schedule.date_range for s in services])
        dates = {d for s in services for d in s.schedule.dates if d in date_range}
        return cls(dates, date_range)
    
    @property
    def is_special(self):
        '''Checks if this schedule is special'''
        return len(self.weekdays) == 0
    
    @property
    def is_today(self):
        return Date.today() in self.dates
    
    @property
    def added_dates(self):
        '''Returns all dates that are added'''
        return {d for d in self.exceptions if d.weekday not in self.weekdays}
    
    @property
    def added_dates_string(self):
        '''Returns a string of all dates that are added'''
        return helpers.flatten_dates(self.added_dates)
    
    @property
    def removed_dates(self):
        '''Returns all dates that are removed'''
        return {d for d in self.exceptions if d.weekday in self.weekdays}
    
    @property
    def removed_dates_string(self):
        '''Returns a string of all dates that are removed'''
        return helpers.flatten_dates(self.removed_dates)
    
    @property
    def has_normal_service(self):
        '''Checks if this schedule indicates normal service'''
        return len(self.weekdays) > 0 or len(self.added_dates) > 0
    
    @property
    def has_no_service(self):
        '''Checks if this schedule indicates no service'''
        return 0 < len(self.weekdays) < 7 or len(self.removed_dates) > 0
    
    def __post_init__(self):
        if len(self.date_range) <= 7:
            self.exceptions = self.dates
        else:
            explicit_weekdays = {d.weekday for d in self.dates}
            for weekday in Weekday:
                included_dates = {d for d in self.dates if d.weekday == weekday}
                excluded_dates = {d for d in self.date_range if d.weekday == weekday and d not in included_dates}
                if len(included_dates) == 0 and len(excluded_dates) == 0:
                    continue
                if len(included_dates) == 1 and len(excluded_dates) == 1:
                    if all(w.is_workday for w in explicit_weekdays):
                        self.weekdays.add(weekday)
                        self.exceptions.update(excluded_dates)
                    else:
                        self.exceptions.update(included_dates)
                elif len(included_dates) >= len(excluded_dates):
                    self.weekdays.add(weekday)
                    self.exceptions.update(excluded_dates)
                else:
                    self.exceptions.update(included_dates)
        
        if self.is_special:
            self.name = 'Special Service'
        elif self.weekdays == {Weekday.MON, Weekday.TUE, Weekday.WED, Weekday.THU, Weekday.FRI, Weekday.SAT, Weekday.SUN}:
            self.name = 'Every Day'
        elif self.weekdays == {Weekday.MON, Weekday.TUE, Weekday.WED, Weekday.THU, Weekday.FRI}:
            self.name = 'Weekdays'
        elif self.weekdays == {Weekday.SAT, Weekday.SUN}:
            self.name = 'Weekends'
        elif len(self.weekdays) == 1:
            self.name = f'{list(self.weekdays)[0].name}s'
        else:
            self.name = '/'.join([w.short_name for w in sorted(self.weekdays)])
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.dates)
    
    def __eq__(self, other):
        return self.dates == other.dates
    
    def __lt__(self, other):
        if self.date_range.start == other.date_range.start:
            if self.is_special and other.is_special:
                return sorted(self.dates) < sorted(other.dates)
            return sorted(self.weekdays) < sorted(other.weekdays)
        return self.date_range < other.date_range
    
    def __contains__(self, date):
        return date in self.dates
    
    def get_weekday_status(self, weekday):
        '''Returns the status class of this schedule on the given weekday'''
        if weekday in self.weekdays:
            return 'normal-service'
        return 'no-service'
    
    def get_date_status(self, date):
        '''Returns the status class of this schedule on the given date'''
        if date in self:
            return 'normal-service'
        return 'no-service'
