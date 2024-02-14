
from enum import IntEnum

class Weekday(IntEnum):
    '''A day of the week'''
    
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6
    
    def __str__(self):
        return self.name
    
    @property
    def name(self):
        '''The full name of this weekday'''
        if self == Weekday.MON:
            return 'Monday'
        if self == Weekday.TUE:
            return 'Tuesday'
        if self == Weekday.WED:
            return 'Wednesday'
        if self == Weekday.THU:
            return 'Thursday'
        if self == Weekday.FRI:
            return 'Friday'
        if self == Weekday.SAT:
            return 'Saturday'
        if self == Weekday.SUN:
            return 'Sunday'
    
    @property
    def short_name(self):
        '''The short name of this weekday'''
        return self.name[0:3]
    
    @property
    def abbreviation(self):
        '''The abbreviation of this weekday'''
        return self.name[0]
    
    @property
    def is_workday(self):
        '''Checks if this weekday is a workday'''
        return self in {Weekday.MON, Weekday.TUE, Weekday.WED, Weekday.THU, Weekday.FRI}
    
    @property
    def is_weekend(self):
        '''Checks if this weekday is a weekend'''
        return self in {Weekday.SAT, Weekday.SUN}
