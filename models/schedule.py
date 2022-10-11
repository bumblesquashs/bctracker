
from datetime import timedelta

import helpers.date

from models.weekday import Weekday

class Schedule:
    '''The days of a week when a service is or is not running within a given date range'''
    
    __slots__ = ('start_date', 'end_date', 'weekdays', 'included_dates', 'excluded_dates', 'name')
    
    @classmethod
    def process(cls, start_date, end_date, weekdays, included_dates, excluded_dates):
        for weekday in Weekday:
            dates = excluded_dates if weekday in weekdays else included_dates
            explicit_dates = {d for d in dates if d.weekday == weekday}
            implicit_dates = get_implicit_dates(weekday, start_date, end_date, explicit_dates)
            if len(explicit_dates) == 0 and len(implicit_dates) == 0:
                if weekday in weekdays:
                    weekdays.remove(weekday)
            elif len(explicit_dates) + len(implicit_dates) == 1:
                if weekday in weekdays:
                    weekdays.remove(weekday)
                    included_dates = included_dates.union(implicit_dates)
            elif len(explicit_dates) > len(implicit_dates):
                if weekday in weekdays:
                    weekdays.remove(weekday)
                    included_dates = included_dates.union(implicit_dates)
                    excluded_dates -= explicit_dates
                else:
                    weekdays.add(weekday)
                    included_dates -= explicit_dates
                    excluded_dates = excluded_dates.union(implicit_dates)
        return cls(start_date, end_date, weekdays, included_dates, excluded_dates)
    
    @classmethod
    def combine(cls, schedules):
        start_date = min({s.start_date for s in schedules})
        end_date = max({s.end_date for s in schedules})
        weekdays = {w for s in schedules for w in s.weekdays}
        included_dates = {d for s in schedules for d in s.included_dates}
        excluded_dates = {d for s in schedules for d in s.excluded_dates}
        modified_dates = included_dates.intersection(excluded_dates)
        return cls(start_date, end_date, weekdays, included_dates - modified_dates, excluded_dates - modified_dates)
    
    def __init__(self, start_date, end_date, weekdays, included_dates, excluded_dates):
        self.start_date = start_date
        self.end_date = end_date
        self.weekdays = weekdays
        self.included_dates = included_dates
        self.excluded_dates = excluded_dates
        
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
            return self.included_dates == other.included_dates
        return self.weekdays == other.weekdays
    
    def __lt__(self, other):
        if self.special and other.special:
            return sorted(self.included_dates) < sorted(other.included_dates)
        return sorted(self.weekdays) < sorted(other.weekdays)
    
    @property
    def special(self):
        return len(self.weekdays) == 0
    
    @property
    def included_dates_string(self):
        '''Returns a formatted string of dates that are included in this schedule'''
        return helpers.date.flatten(sorted(self.included_dates))
    
    @property
    def excluded_dates_string(self):
        '''Returns a formatted string of dates that are excluded from this schedule'''
        return helpers.date.flatten(sorted(self.excluded_dates))
    
    @property
    def date_string(self):
        '''Returns a string indicating the dates that this schedule operates'''
        if self.special and len(self.included_dates) > 0:
            return self.included_dates_string
        if self.start_date == self.end_date:
            return str(self.start_date)
        return f'{self.start_date} to {self.end_date}'
    
    def includes(self, date):
        '''Checks if this schedule includes the given date'''
        if date < self.start_date or date > self.end_date:
            return False
        if date in self.included_dates:
            return True
        if date in self.excluded_dates:
            return False
        return date.weekday in self.weekdays
    
    def get_status(self, weekday):
        '''Returns the status class of this schedue on the given weekday'''
        if weekday in self.weekdays:
            return 'running'
        if len([d for d in self.included_dates if d.weekday == weekday]) > 0:
            return 'limited'
        return 'not-running'

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
