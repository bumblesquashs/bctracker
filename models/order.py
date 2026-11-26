
from dataclasses import dataclass, field

from models.agency import Agency
from models.amenity import Amenity
from models.model import Model
from models.vehicle import Vehicle

import repositories

@dataclass(slots=True)
class Order:
    '''A set of vehicles of a specific model'''
    
    id: int
    agency: Agency
    model: Model | None
    vehicles: list[Vehicle]
    show_all: bool = False
    
    key: tuple = field(init=False)
    years: int = field(init=False)
    visible: bool = field(init=False)
    
    @property
    def context(self):
        '''The context for this order'''
        return self.agency.context
    
    @property
    def years_string(self) -> str:
        if self.years:
            if len(self.years) == 1:
                return str(self.years[0])
            return f'{self.years[0]}-{self.years[-1]}'
        return 'Unknown Year'
    
    @property
    def liveries(self):
        livery_ids = {v.livery for v in self.vehicles if v.livery}
        liveries = {repositories.livery.find(self.agency.id, id) for id in livery_ids}
        return sorted(l for l in liveries if l)
    
    def __post_init__(self):
        self.key = min([b.key for b in self.vehicles])
        self.years = sorted({b.year for b in self.vehicles if b.year})
        self.visible = any(b.visible for b in self.vehicles)
    
    def __str__(self):
        if self.model:
            if self.years:
                if len(self.years) == 1:
                    return f'{self.years[0]} {self.model}'
                return f'{self.years[0]}-{self.years[-1]} {self.model}'
            return str(self.model)
        return 'Unknown year/model'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.agency == other.agency:
            return self.key < other.key
        return self.agency < other.agency
    
    def previous_vehicle(self, vehicle):
        '''The previous vehicle before the given vehicle'''
        try:
            index = self.vehicles.index(vehicle)
            return self.vehicles[index - 1]
        except (IndexError, ValueError):
            return None
    
    def next_vehicle(self, vehicle):
        '''The next vehicle following the given vehicle'''
        try:
            index = self.vehicles.index(vehicle)
            return self.vehicles[index + 1]
        except (IndexError, ValueError):
            return None
    
    @classmethod
    def from_json(cls, order_id: int, agency: Agency, data: dict):
        defaults = agency.order_defaults.copy()
        default_amenities = defaults.pop('amenities', {})
        
        data = defaults | data
        
        model = repositories.model.find(data.pop('model', None))
        order_amenities = data.pop('amenities', {})
        order_vehicles = data.pop('vehicles', [])
        show_all = data.pop('show_all', False)
        
        vehicles: list[Vehicle] = []
        for vehicle_data in order_vehicles:
            vehicle_data = data | vehicle_data
            
            vehicle_amenities = vehicle_data.pop('amenities', {})
            amenities = default_amenities | order_amenities | vehicle_amenities
            vehicle_data['amenities'] = Amenity.parse(amenities)
            
            version = vehicle_data.pop('version', None)
            prefix = vehicle_data.pop('version', None)
            
            if 'id' in vehicle_data:
                ids = [vehicle_data.pop('id')]
            else:
                low = vehicle_data.pop('low')
                high = vehicle_data.pop('high')
                ids = list(range(low, high + 1))
            
            for id in ids:
                name = vehicle_data.pop('name', None)
                vehicle_name_length = agency.config.vehicle_name_length
                if vehicle_name_length:
                    if type(id) is int:
                        if not name:
                            name = f'{id:0{vehicle_name_length}d}'
                        id = str(id)
                    else:
                        id = str(id)
                        if not name:
                            name = id[:vehicle_name_length]
                else:
                    id = str(id)
                    if not name:
                        name = id
                if version:
                    id = f'{id}-{version}'
                if prefix:
                    id = f'{prefix}{id}'
                    name = f'{prefix}{name}'
                vehicles.append(Vehicle(agency, id, name, order_id, model, **vehicle_data))
        return cls(order_id, agency, model, vehicles, show_all)
