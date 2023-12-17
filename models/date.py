
from datetime import datetime, timedelta

import calendar
import pytz

from models.weekday import Weekday

class Date:
    '''A specific year, month, and day'''
    
    __slots__ = (
        'year',
        'month',
        'day',
        'timezone'
    )
    
    @classmethod
    def parse_db(cls, date_string, timezone):
        '''Returns a date parsed from the given string in YYYY-MM-DD format'''
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return cls(date.year, date.month, date.day, timezone)
    
    @classmethod
    def parse_csv(cls, date_string, timezone):
        '''Returns a date parsed from the given string in YYYYMMDD format'''
        date = datetime.strptime(date_string, '%Y%m%d')
        return cls(date.year, date.month, date.day, timezone)
    
    @classmethod
    def today(cls, timezone=None):
        '''Returns the current date'''
        if timezone is None:
            now = datetime.now()
        else:
            now = datetime.now(pytz.timezone(timezone))
        date = now if now.hour >= 4 else now - timedelta(days=1)
        return cls(date.year, date.month, date.day, timezone)
    
    @property
    def is_earlier(self):
        '''Checks if this date is before the current date'''
        return self < Date.today(self.timezone)
    
    @property
    def is_today(self):
        '''Checks if this date is the same as the current date'''
        return self == Date.today(self.timezone)
    
    @property
    def is_later(self):
        '''Checks if this date is after the current date'''
        return self > Date.today(self.timezone)
    
    @property
    def datetime(self):
        '''Returns the datetime equivalent of this date'''
        return datetime(self.year, self.month, self.day)
    
    @property
    def timezone_name(self):
        '''Returns the name of this date's timezone'''
        if self.timezone is None:
            return None
        return datetime.now(pytz.timezone(self.timezone)).tzname()
    
    @property
    def weekday(self):
        '''Returns the weekday of this date'''
        return Weekday(self.datetime.weekday())
    
    def __init__(self, year, month, day, timezone):
        self.year = year
        self.month = month
        self.day = day
        self.timezone = timezone
    
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
        return Date(date.year, date.month, date.day, self.timezone)
    
    def __sub__(self, delta):
        date = self.datetime - delta
        return Date(date.year, date.month, date.day, self.timezone)
    
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
        if self.is_today:
            return 'Today'
        today = Date.today(self.timezone)
        years = today.year - self.year
        if self.month > today.month:
            years -= 1
            months = (today.month + 12) - self.month
        else:
            months = today.month - self.month
        if self.day > today.day:
            months -= 1
            days = (today.day + calendar.monthrange(today.year, today.month)[1]) - self.day
        else:
            days = today.day - self.day
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
    
    def next(self):
        '''Returns the next date'''
        return self + timedelta(days=1)
    
    def previous(self):
        '''Returns the previous date'''
        return self - timedelta(days=1)
