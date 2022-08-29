
from datetime import datetime
import pytz

class Time:
    '''A specific hour, minute, and second'''
    
    __slots__ = ('unknown', 'hour', 'minute', 'second', 'accurate_seconds', 'timezone')
    
    @classmethod
    def parse(cls, time_string, timezone, accurate_seconds=False):
        '''Returns a time parsed from the given string in HH:MM:SS format'''
        if time_string is None or time_string == '':
            return cls(True, 0, 0, 0, False, timezone)
        time_parts = time_string.split(':')
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        if len(time_parts) > 2:
            second = int(time_parts[2])
        else:
            second = 0
            accurate_seconds = False
        return cls(False, hour, minute, second, accurate_seconds, timezone)
    
    @classmethod
    def now(cls, timezone, accurate_seconds=True):
        '''Returns the current time'''
        if timezone is None:
            now = datetime.now()
        else:
            now = datetime.now(pytz.timezone(timezone))
        hour = now.hour
        if hour < 4:
            hour += 24
        return cls(False, hour, now.minute, now.second, accurate_seconds, timezone)
    
    def __init__(self, unknown, hour, minute, second, accurate_seconds, timezone):
        self.unknown = unknown
        self.hour = hour
        self.minute = minute
        self.second = second
        self.accurate_seconds = accurate_seconds
        self.timezone = timezone
    
    def __str__(self):
        if self.unknown:
            return ''
        if self.accurate_seconds:
            return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
        return f'{self.hour:02d}:{self.minute:02d}'
    
    def __eq__(self, other):
        if self.accurate_seconds and other.accurate_seconds:
            return self.hour == other.hour and self.minute == other.minute and self.second == other.second
        return self.hour == other.hour and self.minute == other.minute
    
    def __lt__(self, other):
        if self.hour != other.hour:
            return self.hour < other.hour
        if self.minute != other.minute:
            return self.minute < other.minute
        return self.second < other.second
    
    @property
    def is_earlier(self):
        '''Checks if this time is before the current time'''
        return self < Time.now(self.timezone)
    
    @property
    def is_now(self):
        '''Checks if this time is the same as the current time'''
        return self == Time.now(self.timezone)
    
    @property
    def is_later(self):
        '''Checks if this time is after the current time'''
        return self > Time.now(self.timezone)
    
    @property
    def timezone_name(self):
        if self.timezone is None:
            return None
        return datetime.now(pytz.timezone(self.timezone)).tzname()
    
    def get_minutes(self):
        '''Returns the total number of minutes in this time'''
        return (self.hour * 60) + self.minute
    
    def format_db(self):
        '''Returns a string of this time formatted as HH:MM:SS'''
        if self.unknown:
            return None
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
    
    def format_difference(self, other):
        '''Returns a string of the number of hours and minutes between this time and another time'''
        self_minutes = self.get_minutes()
        other_minutes = other.get_minutes()
        difference = abs(self_minutes - other_minutes)
        
        hour = difference // 60
        minute = difference % 60
        
        parts = []
        if hour > 0:
            parts.append(f'{hour}h')
        if minute > 0:
            parts.append(f'{minute}m')
        if len(parts) == 0:
            return '0h 0m'
        return ' '.join(parts)
