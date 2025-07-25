
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.agency import Agency

from dataclasses import dataclass, field

from models.model import Model

import helpers
import repositories

@dataclass(slots=True)
class Bus:
    '''A public transportation vehicle'''
    
    agency: Agency
    number: int
    name: str
    order_id: int | None = None
    model: Model | None = None
    year: int | None = None
    visible: bool = True
    demo: bool = False,
    livery: str | None = None
    air_conditioned: bool = True
    
    key: tuple = field(init=False)
    
    @property
    def context(self):
        '''The context for this bus'''
        return self.agency.context
    
    @property
    def url_id(self):
        '''The ID to use when making bus URLs'''
        return self.number
    
    @property
    def is_known(self):
        return self.number >= 0
    
    @property
    def year_model(self):
        if self.model:
            if self.year:
                return f'{self.year} {self.model}'
            return str(self.model)
        return None
    
    def __post_init__(self):
        self.key = helpers.key(self.name)
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        return self.number == other.number
    
    def __lt__(self, other):
        return self.key < other.key
    
    def find_decoration(self):
        '''Returns the decoration for this bus, if one exists'''
        return repositories.decoration.find(self.agency.id, self.number)
    
    def find_livery(self):
        '''Returns the livery for this bus, if one exists'''
        if self.livery:
            return repositories.livery.find(self.agency.id, self.livery)
        return None
