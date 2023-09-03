
import helpers.date

from models.daterange import DateRange
from models.weekday import Weekday

class Schedule:
    '''Dates when a service is running'''
    
    __slots__ = ('dates', 'date_range', 'weekdays', 'added_dates', 'removed_dates', 'modified_dates', 'name')
    
    @classmethod
    def combine(cls, schedules, date_range=None):
        '''Returns a schedule that combines other schedules'''
        if len(schedules) == 0:
            return None
        dates = {d for s in schedules for d in s.dates}
        if date_range is None:
            date_range = DateRange(min(dates), max(dates))
        else:
            dates = {d for d in dates if d in date_range}
        modified_dates = {d for s in schedules for d in s.modified_dates}
        for date in dates:
            if len([s for s in schedules if date in s]) < len([s for s in schedules if date in s or date.weekday in s.weekdays]):
                modified_dates.add(date)
        return cls(dates, date_range, modified_dates)
    
    def __init__(self, dates, date_range, modified_dates=None):
        self.dates = dates
        self.date_range = date_range
        if modified_dates is None:
            self.modified_dates = set()
        else:
            self.modified_dates = modified_dates
        self.weekdays = set()
        self.added_dates = set()
        self.removed_dates = set()
        if len(date_range) <= 7:
            self.added_dates.update(dates)
        else:
            for weekday in Weekday:
                explicit_dates = {d for d in dates if d.weekday == weekday}
                implicit_dates = {d for d in self.date_range if d.weekday == weekday and d not in explicit_dates}
                if len(implicit_dates) == 0 and len(explicit_dates) == 0:
                    continue
                if len(explicit_dates) >= len(implicit_dates):
                    self.weekdays.add(weekday)
                    self.removed_dates.update(implicit_dates)
                else:
                    self.added_dates.update(explicit_dates)
        
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
        if self.weekdays == other.weekdays:
            return self.date_range < other.date_range
        return sorted(self.weekdays) < sorted(other.weekdays)
    
    def __contains__(self, date):
        return date in self.dates
    
    @property
    def is_special(self):
        '''Checks if this schedule is special'''
        return len(self.weekdays) == 0
    
    @property
    def all_dates(self):
        '''Returns all exceptions and modified dates'''
        return self.added_dates.union(self.removed_dates).union(self.modified_dates)
    
    @property
    def added_dates_string(self):
        '''Returns a string of all dates that are added'''
        return helpers.date.flatten(self.added_dates)
    
    @property
    def removed_dates_string(self):
        '''Returns a string of all dates that are removed'''
        return helpers.date.flatten(self.removed_dates)
    
    def get_weekday_status(self, weekday):
        '''Returns the status class of this schedule on the given weekday'''
        return 'normal-service' if weekday in self.weekdays else 'no-service'
    
    def get_date_status(self, date):
        '''Returns the status class of this schedule on the given date'''
        if date in self:
            if date in self.modified_dates:
                return 'modified-service'
            return 'normal-service'
        return 'no-service'
    
    def slice(self, date_range):
        '''Returns a version of this schedule limited to the given date range'''
        dates = {d for d in self.dates if d in date_range}
        if len(dates) == 0:
            return None
        modified_dates = [d for d in self.modified_dates if d in dates]
        return Schedule(dates, date_range, modified_dates)
