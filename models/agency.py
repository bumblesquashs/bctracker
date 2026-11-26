
from dataclasses import dataclass, field

from models.config import Config
from models.context import Context
from models.decoration import Decoration
from models.livery import Livery

from constants import *

@dataclass(slots=True)
class Agency:
    '''A company or entity that runs transit'''
    
    id: str
    name: str
    website: str | None = None
    default_system: str | None = None
    decorations: dict[str: Decoration] = field(default_factory=dict)
    liveries: dict[str: Livery] = field(default_factory=dict)
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
    
    def get_decoration(self, id: str) -> Decoration | None:
        try:
            return self.decorations[id]
        except KeyError:
            return None
    
    def get_livery(self, id: str) -> Livery | None:
        try:
            return self.liveries[id]
        except KeyError:
            return None
