
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
    number: str
    name: str
    order_id: int | None = None
    model: Model | None = None
    year: int | None = None
    visible: bool = True
    demo: bool = False,
    livery: str | None = None
    accessible: bool = True
    air_conditioned: bool = True
    usb_charging: bool = False
    cctv: bool = True
    
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
        return not self.number.startswith('-')
    
    @property
    def year_model(self):
        if self.model:
            if self.year:
                return f'{self.year} {self.model}'
            return str(self.model)
        return None
    
    @property
    def has_amenities(self):
        return any([self.accessible, self.air_conditioned, self.usb_charging, self.cctv])
    
    def __post_init__(self):
        self.key = helpers.key(self.name)
    
    def __str__(self):
        if self.is_known:
            return self.name
        return 'Unknown Bus'
    
    def __hash__(self):
        return hash((self.agency, self.number))
    
    def __eq__(self, other):
        return self.agency == other.agency and self.number == other.number and self.order_id == other.order_id
    
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
