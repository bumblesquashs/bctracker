
from enum import IntEnum

class Weekday(IntEnum):
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
        return self.name[0:3]
    
    @property
    def abbreviation(self):
        return self.name[0]
