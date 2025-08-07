
from dataclasses import dataclass
from datetime import datetime, timedelta

import calendar
import pytz

from models.weekday import Weekday

from constants import DEFAULT_TIMEZONE

@dataclass(slots=True)
class Date:
    '''A specific year, month, and day'''
    
    year: int
    month: int
    day: int
    timezone: pytz.BaseTzInfo = DEFAULT_TIMEZONE
    
    @classmethod
    def parse(cls, date_string, timezone=DEFAULT_TIMEZONE, format='%Y-%m-%d'):
        '''Returns a date parsed from a string in the given format'''
        if not date_string:
            return None
        date = datetime.strptime(date_string, format)
        return cls(date.year, date.month, date.day, timezone)
    
    @classmethod
    def today(cls, timezone=DEFAULT_TIMEZONE):
        '''Returns the current date'''
        return cls.fromdatetime(datetime.now(timezone), timezone)
    
    @classmethod
    def fromdatetime(cls, datetime, timezone=DEFAULT_TIMEZONE):
        '''Returns a date from the given datetime'''
        if datetime.hour < 4:
            datetime = datetime - timedelta(days=1)
        return cls(datetime.year, datetime.month, datetime.day, timezone)
    
    @property
    def url_id(self):
        '''The ID to use when making date URLs'''
        return self.format_db()
    
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
        return datetime.now(self.timezone).tzname()
    
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
        return self.year == other.year and self.month == other.month and self.day == other.day and self.timezone == other.timezone
    
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
    
    def format_month(self):
        '''Returns a string of this date formatted as MMMM YYYY'''
        return self.datetime.strftime("%B %Y")
    
    def format_day(self):
        '''Returns a string of this date formatted as DD{ordinal}'''
        day = self.day
        ordinal = "th" if 4 <= day % 100 <= 20 else {1:"st",2:"nd",3:"rd"}.get(day % 10, "th")
        return f'{day}{ordinal}'
    
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
            if months < 0:
                months += 12
                years -= 1
            days = (today.day + calendar.monthrange(self.year, self.month)[1]) - self.day
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
