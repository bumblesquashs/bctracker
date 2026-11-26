
from dataclasses import dataclass, field

from models.config import Config
from models.context import Context

from constants import *

@dataclass(slots=True)
class Agency:
    '''A company or entity that runs transit'''
    
    id: str
    name: str
    website: str | None = None
    default_system: str | None = None
    order_defaults: dict = field(default_factory=dict)
    
    config: Config = field(default_factory=lambda: Config())
    
    @property
    def context(self):
        return Context(agency=self)
    
    @property
    def url_id(self):
        '''The ID to use when making agency URLs'''
        return self.id
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
