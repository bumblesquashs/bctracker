
from dataclasses import dataclass
from datetime import datetime
import pytz

from models.date import Date
from models.time import Time

from constants import DEFAULT_TIMEZONE

@dataclass(slots=True)
class Timestamp:
    
    value: float
    timezone: pytz.BaseTzInfo = DEFAULT_TIMEZONE
    accurate_seconds: bool = True
    
    @classmethod
    def now(cls, timezone=DEFAULT_TIMEZONE, accurate_seconds=True):
        '''Returns the current timestamp'''
        return cls.parse(datetime.now(timezone).timestamp(), timezone, accurate_seconds)
    
    @classmethod
    def parse(cls, value, timezone=DEFAULT_TIMEZONE, accurate_seconds=True):
        '''Returns a timestamp with the given value'''
        if not value:
            return None
        return cls(value, timezone, accurate_seconds)
    
    @property
    def datetime(self):
        '''Returns a datetime from this timestamp'''
        return datetime.fromtimestamp(self.value, self.timezone)
    
    @property
    def date(self):
        '''Returns the date of this timestamp'''
        return Date.fromdatetime(self.datetime, self.timezone)
    
    @property
    def time(self):
        '''Returns the time of this timestamp'''
        return Time.fromdatetime(self.datetime, self.timezone, self.accurate_seconds)
    
    @property
    def is_earlier(self):
        '''Checks if this timestamp is before the current timestamp'''
        return self < Timestamp.now(self.timezone)
    
    @property
    def is_today(self):
        '''Checks if this timestamp is the same as the current date'''
        return self.date.is_today
    
    @property
    def is_now(self):
        '''Checks if this timestamp is the exact current timestamp'''
        return self == Timestamp.now(self.timezone)
    
    @property
    def is_later(self):
        '''Checks if this date is after the current timestamp'''
        return self > Timestamp.now(self.timezone)
    
    @property
    def timezone_name(self):
        '''Returns the name of this timestamp's timezone'''
        return datetime.now(self.timezone).tzname()
    
    def __str__(self):
        date = self.date
        if date.is_today:
            return str(self.time)
        return str(date)
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self and other and self.value == other.value
    
    def __lt__(self, other):
        if not self:
            return False
        if not other:
            return True
        return self.value < other.value
    
    def __gt__(self, other):
        if not self:
            return True
        if not other:
            return False
        return self.value > other.value
    
    def __le__(self, other):
        return self == other or self < other
    
    def __ge__(self, other):
        return self == other or self > other
    
    def __add__(self, value):
        self.value += value
    
    def __sub__(self, value):
        self.value -= value
    
    def format_web(self, time_format='30hr'):
        '''Formats this timestamp for web display'''
        date = self.date
        if date.is_today:
            return f'at {self.time.format_web(time_format)} {self.time.timezone_name}'
        return date.format_since()
