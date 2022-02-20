from datetime import datetime, timedelta
from enum import Enum

import formatting

class Sheet(Enum):
    PREVIOUS = 'previous'
    CURRENT = 'current'
    NEXT = 'next'
    UNKNOWN = 'unknown'

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
        
        self.included_dates = []
        self.excluded_dates = []
        
        self.special = not (mon or tue or wed or thu or fri or sat or sun)
        
        if self.special:
            self.name = 'Special Service'
        elif mon and tue and wed and thu and fri and sat and sun:
            self.name = 'Every Day'
        elif mon and tue and wed and thu and fri and not (sat or sun):
            self.name = 'Weekdays'
        elif mon and not (tue or wed or thu or fri or sat or sun):
            self.name = 'Mondays'
        elif tue and not (mon or wed or thu or fri or sat or sun):
            self.name = 'Tuesdays'
        elif wed and not (mon or tue or thu or fri or sat or sun):
            self.name = 'Wednesdays'
        elif thu and not (mon or tue or wed or fri or sat or sun):
            self.name = 'Thursdays'
        elif fri and not (mon or tue or wed or thu or sat or sun):
            self.name = 'Fridays'
        elif sat and sun and not (mon or tue or wed or thu or fri):
            self.name = 'Weekends'
        elif sat and not (mon or tue or wed or thu or fri or sun):
            self.name = 'Saturdays'
        elif sun and not (mon or tue or wed or thu or fri or sat):
            self.name = 'Sundays'
        else:
            days = []
            if mon:
                days.append('Mon')
            if tue:
                days.append('Tue')
            if wed:
                days.append('Wed')
            if thu:
                days.append('Thu')
            if fri:
                days.append('Fri')
            if sat:
                days.append('Sat')
            if sun:
                days.append('Sun')
            self.name = '/'.join(days)
        
        self.binary_string = ''.join(['1' if d else '0' for d in [mon, tue, wed, thu, fri, sat, sun]])
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.special and other.special and len(self.included_dates) > 0 and len(other.included_dates) > 0:
            return self.included_dates[0] < other.included_dates[0]
        return self.binary_string > other.binary_string
    
    @property
    def sheet(self):
        start = self.start_date.date()
        end = self.end_date.date()
        hour = datetime.now().hour
        today = datetime.today()
        date = (today if hour >= 4 else today - timedelta(days=1)).date()
        
        if start <= date <= end:
            return Sheet.CURRENT
        if end < date:
            return Sheet.PREVIOUS
        if date < start:
            return Sheet.NEXT
        return Sheet.UNKNOWN
    
    @property
    def included_dates_string(self):
        return ', '.join([formatting.long(d) for d in self.included_dates])
    
    @property
    def excluded_dates_string(self):
        return ', '.join([formatting.long(d) for d in self.excluded_dates])
    
    @property
    def date_string(self):
        if self.special:
            return self.included_dates_string
        start = formatting.long(self.start_date)
        end = formatting.long(self.end_date)
        return f'{start} to {end}'
    
    @property
    def is_today(self):
        hour = datetime.now().hour
        today = datetime.today()
        date = (today if hour >= 4 else today - timedelta(days=1)).date()
        if date in self.included_dates:
            return True
        if date in self.excluded_dates:
            return False
        weekday = date.weekday()
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
    
    def add_included_date(self, date):
        self.included_dates.append(date.date())
    
    def add_excluded_date(self, date):
        self.excluded_dates.append(date.date())
