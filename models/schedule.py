
from datetime import timedelta

import helpers.date

from models.daterange import DateRange
from models.weekday import Weekday

class Schedule:
    '''The days of a week when a service is or is not running within a given date range'''
    
    __slots__ = ('date_range', 'weekdays', 'modified_dates', 'excluded_dates', 'name')
    
    @classmethod
    def process(cls, date_range, weekdays, modified_dates, excluded_dates):
        '''Returns a schedule based on the given start date, end date, weekdays, modified dates, and excluded dates'''
        for weekday in Weekday:
            dates = excluded_dates if weekday in weekdays else modified_dates
            explicit_dates = {d for d in dates if d.weekday == weekday}
            implicit_dates = get_implicit_dates(weekday, date_range, explicit_dates)
            if len(explicit_dates) == 0 and len(implicit_dates) == 0:
                if weekday in weekdays:
                    weekdays.remove(weekday)
            elif len(explicit_dates) + len(implicit_dates) == 1:
                if weekday in weekdays:
                    weekdays.remove(weekday)
                    modified_dates = modified_dates.union(implicit_dates)
            elif len(explicit_dates) > len(implicit_dates):
                if weekday in weekdays:
                    weekdays.remove(weekday)
                    modified_dates = modified_dates.union(implicit_dates)
                    excluded_dates -= explicit_dates
                else:
                    weekdays.add(weekday)
                    modified_dates -= explicit_dates
                    excluded_dates = excluded_dates.union(implicit_dates)
        return cls(date_range, weekdays, modified_dates, excluded_dates)
    
    @classmethod
    def combine(cls, schedules):
        '''Returns a schedule that combines the values of list of other schedules'''
        if len(schedules) == 0:
            return None
        date_range = DateRange.combine([s.date_range for s in schedules])
        weekdays = {w for s in schedules for w in s.weekdays}
        modified_dates = {d for s in schedules for d in s.modified_dates}
        excluded_dates = {d for s in schedules for d in s.excluded_dates}
        for date in excluded_dates:
            if len([s for s in schedules if date in s.excluded_dates]) < len([s for s in schedules if date.weekday in s.weekdays]):
                modified_dates.add(date)
        return cls(date_range, weekdays, modified_dates, excluded_dates - modified_dates)
    
    def __init__(self, date_range, weekdays, modified_dates, excluded_dates):
        self.date_range = date_range
        self.weekdays = weekdays
        self.modified_dates = modified_dates
        self.excluded_dates = excluded_dates
        
        if self.special:
            self.name = 'Special Service'
        elif weekdays == {Weekday.MON, Weekday.TUE, Weekday.WED, Weekday.THU, Weekday.FRI, Weekday.SAT, Weekday.SUN}:
            self.name = 'Every Day'
        elif weekdays == {Weekday.MON, Weekday.TUE, Weekday.WED, Weekday.THU, Weekday.FRI}:
            self.name = 'Weekdays'
        elif weekdays == {Weekday.SAT, Weekday.SUN}:
            self.name = 'Weekends'
        elif len(weekdays) == 1:
            self.name = f'{list(weekdays)[0].name}s'
        else:
            self.name = '/'.join([w.short_name for w in sorted(weekdays)])
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if self.special and other.special:
            return self.modified_dates == other.modified_dates
        return self.weekdays == other.weekdays
    
    def __lt__(self, other):
        if self.special and other.special:
            return sorted(self.modified_dates) < sorted(other.modified_dates)
        if self.special:
            return False
        if other.special:
            return True
        return sorted(self.weekdays) < sorted(other.weekdays)
    
    @property
    def special(self):
        '''Checks if this schedule is special service'''
        return len(self.weekdays) == 0
    
    @property
    def modified_dates_string(self):
        '''Returns a formatted string of dates that are modified in this schedule'''
        return helpers.date.flatten(sorted(self.modified_dates))
    
    @property
    def excluded_dates_string(self):
        '''Returns a formatted string of dates that are excluded from this schedule'''
        return helpers.date.flatten(sorted(self.excluded_dates))
    
    def includes(self, date):
        '''Checks if this schedule includes the given date'''
        if date not in self.date_range:
            return False
        if date in self.modified_dates:
            return True
        if date in self.excluded_dates:
            return False
        return date.weekday in self.weekdays
    
    def get_weekday_status(self, weekday):
        '''Returns the status class of this schedule on the given weekday'''
        return 'normal-service' if weekday in self.weekdays else 'no-service'
    
    def get_date_status(self, date):
        '''Returns the status class of this schedule on the given date'''
        if self.includes(date):
            if date in self.modified_dates:
                return 'modified-service'
            return 'normal-service'
        return 'no-service'

def get_implicit_dates(weekday, date_range, explicit_dates):
    '''Returns dates on the given weekday within the date range that are not included in the explicit dates'''
    implicit_dates = set()
    date = date_range.start
    while date.weekday != weekday:
        date += timedelta(days=1)
    while date in date_range:
        if date not in explicit_dates:
            implicit_dates.add(date)
        date += timedelta(weeks=1)
    return implicit_dates
