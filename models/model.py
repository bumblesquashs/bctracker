
from dataclasses import dataclass, field
from enum import Enum

class ModelCategory(Enum):
    '''A category of vehicle model'''
    
    BUS = 'Bus'
    TRAIN = 'Train'
    FERRY = 'Vessel'
    VEHICLE = 'Vehicle'
    
    @property
    def icon(self) -> str:
        return f'model/category/{self.name.lower()}'
    
    @property
    def prefix_title(self) -> bool:
        match self:
            case ModelCategory.BUS:
                return True
            case ModelCategory.TRAIN:
                return True
            case ModelCategory.FERRY:
                return False
            case ModelCategory.VEHICLE:
                return False
    
    def __str__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value

class ModelType(Enum):
    '''A type of vehicle model'''
    
    ARTIC_BUS = 'Articulated Bus'
    COACH_BUS = 'Coach Bus'
    CONVENTIONAL_BUS = 'Conventional Bus'
    DOUBLE_DECKER_BUS = 'Double Decker Bus'
    MIDI_BUS = 'Midibus'
    SHUTTLE_BUS = 'Shuttle Bus'
    TROLLEY_BUS = 'Trolley Bus'
    
    RORO_FERRY = 'Roll On/Roll Off Ferry'
    PASSENGER_FERRY = 'Passenger Ferry'
    
    @property
    def icon(self) -> str:
        return f'model/type/{self.name.lower()}'.replace('_', '-')
    
    @property
    def category(self) -> ModelCategory:
        match self:
            case ModelType.ARTIC_BUS:
                return ModelCategory.BUS
            case ModelType.COACH_BUS:
                return ModelCategory.BUS
            case ModelType.CONVENTIONAL_BUS:
                return ModelCategory.BUS
            case ModelType.DOUBLE_DECKER_BUS:
                return ModelCategory.BUS
            case ModelType.MIDI_BUS:
                return ModelCategory.BUS
            case ModelType.SHUTTLE_BUS:
                return ModelCategory.BUS
            case ModelType.SHUTTLE_BUS:
                return ModelCategory.BUS
            case ModelType.TROLLEY_BUS:
                return ModelCategory.BUS
            case ModelType.RORO_FERRY:
                return ModelCategory.FERRY
            case ModelType.PASSENGER_FERRY:
                return ModelCategory.FERRY
    
    def __str__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        if self.category == other.category:
            return self.value < other.value
        return self.category < other.category

@dataclass(slots=True)
class Model:
    '''A specific version of a vehicle'''
    
    id: str
    type: ModelType
    name: str
    manufacturer: str | None = None
    length: float | None = None
    length_units: str | None = None
    fuel: str | None = None
    capacity: dict[str, str] = field(default_factory=dict)
    
    @property
    def icon(self) -> str:
        return self.type.icon
    
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
