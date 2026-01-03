
from dataclasses import dataclass
from enum import Enum

class LogLevel(Enum):
    
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
    
    @classmethod
    def parse(cls, value: str):
        try:
            return cls(value.lower())
        except:
            return None
    
    def __str__(self):
        return self.value.title()

@dataclass(slots=True)
class Log:
    
    timestamp: str
    level: LogLevel
    message: str
    
    @classmethod
    def from_line(cls, line: str):
        parts = line.split(': ', 1)
        data = parts[0]
        message = parts[1]
        data_parts = data.split('] ', 1)
        timestamp = data_parts[0][1:]
        level = LogLevel.parse(data_parts[1])
        return cls(timestamp, level, message)
