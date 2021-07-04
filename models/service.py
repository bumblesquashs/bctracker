from datetime import datetime, timedelta
from enum import IntEnum

from formatting import format_date

class ServiceType(IntEnum):
    WEEKDAY = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    WEEKDAY_EXCEPT_FRIDAY = 5
    FRI = 6
    WEEKEND = 7
    SAT = 8
    SUN = 9
    SPECIAL = 10
    UNKNOWN = 11

class Service:
    def __init__(self, system, service_id, start_date, end_date, mon, tue, wed, thu, fri, sat, sun):
        self.system = system
        self.id = service_id
        self.start_date = start_date
        self.end_date = end_date

        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun

        self.special_dates = []
        self.excluded_dates = []

        if sat and sun:
            self.type = ServiceType.WEEKEND
        elif mon and tue and wed and thu and fri:
            self.type = ServiceType.WEEKDAY
        elif mon and tue and wed and thu and (not fri):
            self.type = ServiceType.WEEKDAY_EXCEPT_FRIDAY
        elif mon:
            self.type = ServiceType.MON
        elif tue:
            self.type = ServiceType.TUE
        elif wed:
            self.type = ServiceType.WED
        elif thu:
            self.type = ServiceType.THU
        elif fri:
            self.type = ServiceType.FRI
        elif sat:
            self.type = ServiceType.SAT
        elif sun:
            self.type = ServiceType.SUN
        elif not (mon or tue or wed or thu or fri or sat or sun):
            self.type = ServiceType.SPECIAL
        else:
            self.type = ServiceType.UNKNOWN
    
    def __str__(self):
        if self.type == ServiceType.WEEKDAY:
            return 'Weekdays'
        elif self.type == ServiceType.MON:
            return 'Mondays'
        elif self.type == ServiceType.TUE:
            return 'Tuesdays'
        elif self.type == ServiceType.WED:
            return 'Wednesdays'
        elif self.type == ServiceType.THU:
            return 'Thursdays'
        elif self.type == ServiceType.WEEKDAY_EXCEPT_FRIDAY:
            return 'Weekdays except Friday'
        elif self.type == ServiceType.FRI:
            return 'Fridays'
        elif self.type == ServiceType.WEEKEND:
            return 'Weekends'
        elif self.type == ServiceType.SAT:
            return 'Saturdays'
        elif self.type == ServiceType.SUN:
            return 'Sundays'
        elif self.type == ServiceType.SPECIAL:
            return self.special_dates_string
        else:
            return 'Unknown'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.type < other.type
    
    @property
    def special_dates_string(self):
        return ', '.join(self.special_dates)
    
    @property
    def excluded_dates_string(self):
        return ', '.join(self.excluded_dates)

    @property
    def date_string(self):
        if self.type == ServiceType.SPECIAL:
            return 'Special Service'
        start = format_date(self.start_date)
        end = format_date(self.end_date)
        return f'{start} to {end}'
    
    @property
    def is_current(self):
        return self.start_date.date() <= datetime.now().date() <= self.end_date.date()
    
    @property
    def is_today(self):
        hour = datetime.now().hour
        today = datetime.today()
        date = today if hour >= 5 else today - timedelta(days=1)
        date_string = format_date(date)
        if date_string in self.special_dates:
            return True
        if date_string in self.excluded_dates:
            return False
        weekday = date.date().weekday()
        if weekday == 0:
            return self.mon
        if weekday == 1:
            return self.tue
        if weekday == 2:
            return self.wed
        if weekday == 3:
            return self.thu
        if weekday == 4:
            return self.fri
        if weekday == 5:
            return self.sat
        if weekday == 6:
            return self.sun
        return False
    
    def add_special_date(self, date):
        self.special_dates.append(format_date(date))
    
    def add_excluded_date(self, date):
        self.excluded_dates.append(format_date(date))
