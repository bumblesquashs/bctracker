
from enum import Enum

class BusModelType(Enum):
    artic = "Articulated"
    conventional = "Conventional"
    decker = "Double Decker"
    shuttle = "Shuttle"
    
    def __str__(self):
        return self.value

class BusModel:
    __slots__ = ('id', 'manufacturer', 'name', 'length', 'fuel', 'type')
    
    @classmethod
    def from_csv(cls, row):
        id = row['model_id']
        manufacturer = row['manufacturer']
        name = row['name']
        length = float(row['length'])
        fuel = row['fuel']
        type = BusModelType[row['type']]
        return cls(id, manufacturer, name, length, fuel, type)
    
    def __init__(self, id, manufacturer, name, length, fuel, type):
        self.id = id
        self.manufacturer = manufacturer
        self.name = name
        self.length = length
        self.fuel = fuel
        self.type = type
    
    def __str__(self):
        return f'{self.manufacturer} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
