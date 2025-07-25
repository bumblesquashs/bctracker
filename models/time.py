
from dataclasses import dataclass
from datetime import datetime
import pytz

from constants import DEFAULT_TIMEZONE

@dataclass(slots=True)
class Time:
    '''A specific hour, minute, and second'''
    
    hour: int | None
    minute: int | None
    second: int | None
    timezone: pytz.BaseTzInfo = DEFAULT_TIMEZONE
    
    @classmethod
    def parse(cls, time_string, timezone=DEFAULT_TIMEZONE, accurate_seconds=False):
        '''Returns a time parsed from the given string in HH:MM:SS format'''
        if not time_string:
            return cls.unknown(timezone)
        time_parts = time_string.split(':')
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        if len(time_parts) > 2 and accurate_seconds:
            second = int(time_parts[2])
        else:
            second = None
        return cls(hour, minute, second, timezone)
    
    @classmethod
    def now(cls, timezone=DEFAULT_TIMEZONE, accurate_seconds=True):
        '''Returns the current time'''
        return cls.fromdatetime(datetime.now(timezone), timezone, accurate_seconds)
    
    @classmethod
    def fromdatetime(cls, datetime, timezone=DEFAULT_TIMEZONE, accurate_seconds=True):
        '''Returns a time from the given datetime'''
        hour = datetime.hour
        if hour < 4:
            hour += 24
        if accurate_seconds:
            second = datetime.second
        else:
            second = None
        return cls(hour, datetime.minute, second, timezone)
    
    @classmethod
    def unknown(cls, timezone=DEFAULT_TIMEZONE):
        '''Returns an unknown time'''
        return cls(None, None, None, timezone)
    
    @property
    def is_unknown(self):
        '''Checks if this time is unknown'''
        return self.hour is None or self.minute is None
    
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
    def datetime(self):
        '''Returns the datetime equivalent of this time'''
        hour = self.hour
        while hour >= 24:
            hour -= 24
        second = self.second
        if second is None:
            second = 0
        return datetime(2000, 1, 1, hour, self.minute, second)
    
    @property
    def timezone_name(self):
        '''Returns the name of this time's timezone'''
        return datetime.now(self.timezone).tzname()
    
    def __str__(self):
        return self.format_web()
    
    def __eq__(self, other):
        return other and self.hour == other.hour and self.minute == other.minute and self.second == other.second
    
    def __lt__(self, other):
        if self.is_unknown:
            return True
        if not other or other.is_unknown:
            return False
        if self.hour != other.hour:
            return self.hour < other.hour
        if self.minute != other.minute:
            return self.minute < other.minute
        if self.second is None:
            return False
        if other.second is None:
            return True
        return self.second < other.second
    
    def __gt__(self, other):
        if self.is_unknown:
            return False
        if not other or other.is_unknown:
            return True
        if self.hour != other.hour:
            return self.hour > other.hour
        if self.minute != other.minute:
            return self.minute > other.minute
        if self.second is None:
            return True
        if other.second is None:
            return False
        return self.second > other.second
    
    def __le__(self, other):
        return self < other or self == other
    
    def __ge__(self, other):
        return self > other or self == other
    
    def __add__(self, delta):
        time = self.datetime + delta
        hour = time.hour
        while hour < 4:
            hour += 24
        second = time.second
        if self.second is None:
            second = None
        return Time(hour, time.minute, second, self.timezone)
    
    def __sub__(self, delta):
        time = self.datetime - delta
        hour = time.hour
        while hour < 4:
            hour += 24
        second = time.second
        if self.second is None:
            second = None
        return Time(hour, time.minute, second, self.timezone)
    
    def get_minutes(self, round_seconds=False):
        '''Returns the total number of minutes in this time'''
        if self.is_unknown:
            return 0
        minutes = (self.hour * 60) + self.minute
        if round_seconds and self.second is not None and self.second >= 30:
            minutes += 1
        return minutes
    
    def format_db(self):
        '''Returns a string of this time formatted as HH:MM:SS'''
        if self.is_unknown:
            return None
        if self.second is None:
            return f'{self.hour:02d}:{self.minute:02d}'
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
    
    def format_web(self, time_format='30hr'):
        '''Formats this time for web display'''
        if self.is_unknown:
            return ''
        hour = self.hour
        minute = self.minute
        second = self.second
        if time_format == '12hr':
            if hour < 4:
                hour_str = '12' if hour == 0 else str(hour)
                am_pm = 'xm'
            elif hour < 12:
                hour_str = str(hour)
                am_pm = 'am'
            elif hour < 24:
                hour_str = '12' if hour == 12 else str(hour - 12)
                am_pm = 'pm'
            else:
                hour_str = '12' if hour == 24 else str(hour - 24)
                am_pm = 'xm'
            if second is None:
                return f'{hour_str}:{minute:02d}{am_pm}'
            return f'{hour_str}:{minute:02d}:{second:02d}{am_pm}'
        if second is None:
            return f'{hour:02d}:{minute:02d}'
        return f'{hour:02d}:{minute:02d}:{second:02d}'
    
    def format_difference(self, other):
        '''Returns a string of the number of hours and minutes between this time and another time'''
        if self.is_unknown or other.is_unknown:
            return ''
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
        if parts:
            return ' '.join(parts)
        return '0h 0m'
