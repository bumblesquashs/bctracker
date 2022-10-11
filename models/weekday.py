
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
        if self == Weekday.MON:
            return 'Mon'
        if self == Weekday.TUE:
            return 'Tue'
        if self == Weekday.WED:
            return 'Wed'
        if self == Weekday.THU:
            return 'Thu'
        if self == Weekday.FRI:
            return 'Fri'
        if self == Weekday.SAT:
            return 'Sat'
        if self == Weekday.SUN:
            return 'Sun'
