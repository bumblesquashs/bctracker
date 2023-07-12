
from enum import Enum

class ModelType(Enum):
    '''A type of vehicle model'''
    
    artic = "Articulated"
    conventional = "Conventional"
    decker = "Double Decker"
    midibus = "Midibus"
    shuttle = "Shuttle"
    test = "Test"
    
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
    
    __slots__ = ('id', 'manufacturer', 'name', 'length', 'fuel', 'type')
    
    @classmethod
    def from_csv(cls, row):
        '''Returns a model initialized from the given CSV row'''
        id = row['model_id']
        manufacturer = row['manufacturer']
        name = row['name']
        length = float(row['length'])
        fuel = row['fuel']
        type = ModelType[row['type']]
        return cls(id, manufacturer, name, length, fuel, type)
    
    def __init__(self, id, manufacturer, name, length, fuel, type):
        self.id = id
        self.manufacturer = manufacturer
        self.name = name
        self.length = length
        self.fuel = fuel
        self.type = type
    
    def __str__(self):
        return f'{self.display_manufacturer} {self.display_name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
    
    @property
    def display_manufacturer(self):
        '''Formats the manufacturer for web display'''
        return self.manufacturer.replace('/', '/<wbr />')
    
    @property
    def display_name(self):
        '''Formats the model name for web display'''
        return self.name.replace('/', '/<wbr />')
    
    @property
    def is_test(self):
        '''Checks if this is a test model'''
        return self.type == ModelType.test
