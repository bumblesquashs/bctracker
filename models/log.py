
from dataclasses import dataclass

@dataclass(slots=True)
class Log:
    '''A log of an event that occurred'''
    
    timestamp: str
    level: str
    message: str
