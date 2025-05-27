
from dataclasses import dataclass

from models.date import Date

@dataclass(slots=True)
class Event:
    '''Something that occurred on a specific date'''
    
    date: Date
    name: str
    description: str | None = None
    
    @property
    def is_today(self):
        return self.date.is_today
