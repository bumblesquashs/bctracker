
from datetime import datetime

class Time:
    
    def __init__(self, time_string):
        if time_string is None or time_string == '':
            self.unknown = True
            self.hour = -1
            self.minute = 0
            self.second = 0
        else:
            self.unknown = False
            time_parts = time_string.split(':')
            
            self.hour = int(time_parts[0])
            self.minute = int(time_parts[1])
            if len(time_parts) > 2:
                self.second = int(time_parts[2])
            else:
                self.second = 0
    
    def __str__(self):
        if self.unknown:
            return ''
        if self.second == 0:
            return f'{self.hour:02d}:{self.minute:02d}'
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
    
    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute and self.second == other.second
    
    def __lt__(self, other):
        if self.hour != other.hour:
            return self.hour < other.hour
        if self.minute != other.minute:
            return self.minute < other.minute
        return self.second < other.second
    
    @property
    def full_string(self):
        if self.unknown:
            return ''
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
    
    @property
    def is_earlier(self):
        return self.get_minutes() < get_current_minutes()
    
    @property
    def is_now(self):
        return self.get_minutes() == get_current_minutes()
    
    @property
    def is_later(self):
        return self.get_minutes() > get_current_minutes()
    
    def get_minutes(self):
        return (self.hour * 60) + self.minute
    
    def get_difference(self, other):
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

def get_current_minutes():
    now = datetime.now()
    hour = now.hour
    if hour < 4:
        hour += 24
    return (hour * 60) + now.minute
