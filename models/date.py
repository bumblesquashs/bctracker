
from datetime import datetime, timedelta
from pytz import timezone

import calendar

class Date:
    '''A specific year, month, and day'''
    
    __slots__ = ('year', 'month', 'day')
    
    @classmethod
    def parse_db(cls, date_string):
        '''Returns a date parsed from the given string in YYYY-MM-DD format'''
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return cls(date.year, date.month, date.day)
    
    @classmethod
    def parse_csv(cls, date_string):
        '''Returns a date parsed from the given string in YYYYMMDD format'''
        date = datetime.strptime(date_string, '%Y%m%d')
        return cls(date.year, date.month, date.day)
    
    @classmethod
    def today(cls, system=None):
        '''Returns the current date'''
        if system is not None and system.timezone is not None:
            now = datetime.now(timezone(system.timezone))
        else:
            now = datetime.now()
        date = now if now.hour >= 4 else now - timedelta(days=1)
        return cls(date.year, date.month, date.day)
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def __str__(self):
        return self.format_long()
    
    def __hash__(self):
        return hash((self.year, self.month, self.day))
    
    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day
    
    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        return self.day < other.day
    
    def __gt__(self, other):
        if self.year != other.year:
            return self.year > other.year
        if self.month != other.month:
            return self.month > other.month
        return self.day > other.day
    
    def __le__(self, other):
        return self < other or self == other
    
    def __ge__(self, other):
        return self > other or self == other
    
    def __add__(self, delta):
        date = self.datetime + delta
        return Date(date.year, date.month, date.day)
    
    def __sub__(self, delta):
        date = self.datetime - delta
        return Date(date.year, date.month, date.day)
    
    @property
    def datetime(self):
        '''Returns the datetime equivalent of this date'''
        return datetime(self.year, self.month, self.day)
    
    @property
    def weekday(self):
        '''Returns the weekday of this date'''
        return self.datetime.weekday()
    
    def format_db(self):
        '''Returns a string of this date formatted as YYYY-MM-DD'''
        return self.datetime.strftime('%Y-%m-%d')
    
    def format_long(self):
        '''Returns a string of this date formatted as MMMM DD, YYYY'''
        if self.year == datetime.now().year:
            return self.datetime.strftime('%B %-d')
        return self.datetime.strftime('%B %-d, %Y')
    
    def format_short(self):
        '''Returns a string of this date formatted as MMM DD, YYYY'''
        if self.year == datetime.now().year:
            return self.datetime.strftime("%b %-d")
        return self.datetime.strftime("%b %-d, %Y")
    
    def format_since(self):
        '''Returns a string of the number of days, months, and years since this date'''
        now = datetime.now()
        years = now.year - self.year
        if self.month > now.month:
            years -= 1
            months = (now.month + 12) - self.month
        else:
            months = now.month - self.month
        if self.day > now.day:
            months -= 1
            days = (now.day + calendar.monthrange(now.year, now.month)[1]) - self.day
        else:
            days = now.day - self.day
        parts = []
        if years == 1:
            parts.append('1 year')
        elif years > 1:
            parts.append(f'{years} years')
        if months == 1:
            parts.append('1 month')
        elif months > 1:
            parts.append(f'{months} months')
        if days == 1:
            parts.append('1 day')
        elif days > 1 or len(parts) == 0:
            parts.append(f'{days} days')
        return ', '.join(parts) + ' ago'
