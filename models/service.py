from datetime import datetime, timedelta
from enum import Enum

import formatting

class Sheet(Enum):
    PREVIOUS = 'previous'
    CURRENT = 'current'
    NEXT = 'next'
    UNKNOWN = 'unknown'

class Service:
    __slots__ = ('system', 'id', 'start_date', 'end_date', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'included_dates', 'excluded_dates', 'special', 'name', 'binary_string')
    
    def __init__(self, system, row):
        self.system = system
        self.id = row['service_id']
        self.start_date = formatting.csv(row['start_date'])
        self.end_date = formatting.csv(row['end_date'])
        self.mon = row['monday'] == '1'
        self.tue = row['tuesday'] == '1'
        self.wed = row['wednesday'] == '1'
        self.thu = row['thursday'] == '1'
        self.fri = row['friday'] == '1'
        self.sat = row['saturday'] == '1'
        self.sun = row['sunday'] == '1'
        
        self.included_dates = []
        self.excluded_dates = []
        
        self.special = not (self.mon or self.tue or self.wed or self.thu or self.fri or self.sat or self.sun)
        
        if self.special:
            self.name = 'Special Service'
        elif self.mon and self.tue and self.wed and self.thu and self.fri and self.sat and self.sun:
            self.name = 'Every Day'
        elif self.mon and self.tue and self.wed and self.thu and self.fri and not (self.sat or self.sun):
            self.name = 'Weekdays'
        elif self.mon and not (self.tue or self.wed or self.thu or self.fri or self.sat or self.sun):
            self.name = 'Mondays'
        elif self.tue and not (self.mon or self.wed or self.thu or self.fri or self.sat or self.sun):
            self.name = 'Tuesdays'
        elif self.wed and not (self.mon or self.tue or self.thu or self.fri or self.sat or self.sun):
            self.name = 'Wednesdays'
        elif self.thu and not (self.mon or self.tue or self.wed or self.fri or self.sat or self.sun):
            self.name = 'Thursdays'
        elif self.fri and not (self.mon or self.tue or self.wed or self.thu or self.sat or self.sun):
            self.name = 'Fridays'
        elif self.sat and self.sun and not (self.mon or self.tue or self.wed or self.thu or self.fri):
            self.name = 'Weekends'
        elif self.sat and not (self.mon or self.tue or self.wed or self.thu or self.fri or self.sun):
            self.name = 'Saturdays'
        elif self.sun and not (self.mon or self.tue or self.wed or self.thu or self.fri or self.sat):
            self.name = 'Sundays'
        else:
            days = []
            if self.mon:
                days.append('Mon')
            if self.tue:
                days.append('Tue')
            if self.wed:
                days.append('Wed')
            if self.thu:
                days.append('Thu')
            if self.fri:
                days.append('Fri')
            if self.sat:
                days.append('Sat')
            if self.sun:
                days.append('Sun')
            self.name = '/'.join(days)
        
        self.binary_string = ''.join(['1' if d else '0' for d in [self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun]])
    
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
