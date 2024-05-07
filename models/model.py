
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

class Model:
    '''A specific version of a vehicle'''
    
    __slots__ = (
        'id',
        'type',
        'name',
        'manufacturer',
        'length',
        'fuel'
    )
    
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
    
    def __init__(self, id, type, name, **kwargs):
        self.id = id
        self.type = type
        self.name = name
        self.manufacturer = kwargs.get('manufacturer')
        self.length = kwargs.get('length')
        self.fuel = kwargs.get('fuel')
    
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
