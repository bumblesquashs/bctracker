
import helpers.date

from models.daterange import DateRange
from models.weekday import Weekday

class Schedule:
    '''Dates when a service is running'''
    
    __slots__ = ('date_range', 'weekdays', 'exceptions', 'modifications', 'name')
    
    @classmethod
    def combine(cls, schedules, date_range=None, weekdays=None, exceptions=None, modifications=None):
        '''Returns a schedule that combines other schedules'''
        if len(schedules) == 0:
            if date_range is None:
                return None
            return cls(date_range, set(), set(), set())
        if date_range is None:
            date_range = DateRange.combine([s.date_range for s in schedules])
        if weekdays is None:
            weekdays = {w for s in schedules for w in s.weekdays}
        if modifications is None:
            modifications = {d for s in schedules for d in s.modifications}
        if exceptions is None:
            added_dates = {d for s in schedules for d in s.added_dates}
            removed_dates = {d for s in schedules for d in s.removed_dates}
            fully_removed_dates = set()
            for weekday in Weekday:
                dates = [s.removed_dates for s in schedules if weekday in s.weekdays]
                if len(dates) > 0:
                    fully_removed_dates.update(set.intersection(*dates))
            fully_removed_dates.difference_update(added_dates)
            modifications.update(added_dates)
            modifications.update(removed_dates.difference(fully_removed_dates))
            added_dates = {d for d in added_dates if d.weekday not in weekdays}
            removed_dates = {d for d in fully_removed_dates if d.weekday in weekdays}
            exceptions = added_dates.union(removed_dates)
        return cls(date_range, weekdays, exceptions, modifications)
    
    def __init__(self, date_range, weekdays, exceptions, modifications):
        exceptions = {d for d in exceptions if d in date_range}
        modifications = {d for d in modifications if d in date_range}
        for weekday in Weekday:
            explicit_dates = {d for d in exceptions if d.weekday == weekday}
            implicit_dates = {d for d in date_range if d.weekday == weekday and d not in explicit_dates}
            if len(implicit_dates) == 0 and len(explicit_dates) == 0:
                if weekday in weekdays:
                    weekdays.remove(weekday)
            elif len(implicit_dates) + len(explicit_dates) == 1:
                if weekday in weekdays:
                    weekdays.remove(weekday)
                    exceptions.difference_update(explicit_dates)
                    exceptions.update(implicit_dates)
            elif len(explicit_dates) > len(implicit_dates):
                if weekday in weekdays:
                    weekdays.remove(weekday)
                else:
                    weekdays.add(weekday)
                exceptions.difference_update(explicit_dates)
                exceptions.update(implicit_dates)
        self.date_range = date_range
        self.weekdays = weekdays
        self.exceptions = exceptions
        self.modifications = modifications
        
        if self.is_special:
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
    
    def __hash__(self):
        return hash((self.date_range, self.weekdays, self.exceptions))
    
    def __eq__(self, other):
        return self.date_range == other.date_range and self.weekdays == other.weekdays and self.exceptions == other.exceptions
    
    def __lt__(self, other):
        if self.date_range == other.date_range:
            if self.weekdays == other.weekdays:
                return sorted(self.exceptions) < sorted(other.exceptions)
            return sorted(self.weekdays) < sorted(other.weekdays)
        return self.date_range < other.date_range
    
    def __contains__(self, date):
        if date in self.date_range:
            if date.weekday in self.weekdays:
                return date not in self.exceptions
            return date in self.exceptions
        return False
    
    @property
    def is_special(self):
        return len(self.weekdays) == 0
    
    @property
    def is_empty(self):
        return len(self.weekdays) == 0 and len(self.exceptions) == 0
    
    @property
    def added_dates(self):
        return {d for d in self.exceptions if d.weekday not in self.weekdays}
    
    @property
    def added_dates_string(self):
        return helpers.date.flatten(self.added_dates)
    
    @property
    def removed_dates(self):
        return {d for d in self.exceptions if d.weekday in self.weekdays}
    
    @property
    def removed_dates_string(self):
        return helpers.date.flatten(self.removed_dates)
    
    def get_weekday_status(self, weekday):
        '''Returns the status class of this schedule on the given weekday'''
        return 'normal-service' if weekday in self.weekdays else 'no-service'
    
    def get_date_status(self, date):
        '''Returns the status class of this schedule on the given date'''
        if date in self:
            if date in self.modifications:
                return 'modified-service'
            return 'normal-service'
        return 'no-service'
    
    def slice(self, date_range):
        return Schedule(date_range, self.weekdays.copy(), self.exceptions.copy(), self.modifications.copy())
