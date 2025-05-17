
from dataclasses import dataclass
from enum import Enum

class ModelType(Enum):
    '''A type of vehicle model'''
    
    artic = "Articulated"
    conventional = "Conventional"
    decker = "Double Decker"
    midibus = "Midibus"
    shuttle = "Shuttle"
    
    def __str__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value

@dataclass(slots=True)
class Model:
    '''A specific version of a vehicle'''
    
    id: str
    type: ModelType
    name: str
    manufacturer: str | None = None
    length: float | None = None
    fuel: str | None = None
    
    @property
    def display_manufacturer(self):
        '''Formats the manufacturer for web display'''
        if self.manufacturer:
            return self.manufacturer.replace('/', '/<wbr />')
        return None
    
    @property
    def display_name(self):
        '''Formats the model name for web display'''
        return self.name.replace('/', '/<wbr />')
    
    def __str__(self):
        if self.manufacturer:
            return f'{self.display_manufacturer} {self.display_name}'
        return self.display_name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
