
from dataclasses import dataclass, field

from models.agency import Agency
from models.model import Model
from models.vehicle import Vehicle

@dataclass(slots=True)
class Order:
    '''A set of vehicles of a specific model'''
    
    id: int
    agency: Agency
    model: Model | None
    vehicles: list[Vehicle]
    
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
    
    def __post_init__(self):
        self.key = min([b.key for b in self.vehicles])
        self.years = sorted({b.year for b in self.vehicles})
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
    def from_json(cls, order_id: int, agency: Agency, model: Model | None, rows: list):
        vehicles = []
        for row in rows:
            if 'id' in row:
                id = row['id']
                del row['id']
                try:
                    name = row['name']
                    del row['name']
                except:
                    name = None
                if agency.vehicle_name_length:
                    if type(id) is int:
                        if not name:
                            name = f'{id:0{agency.vehicle_name_length}d}'
                        id = str(id)
                    else:
                        id = str(id)
                        if not name:
                            name = id[:agency.vehicle_name_length]
                else:
                    id = str(id)
                    if not name:
                        name = id
                vehicles.append(Vehicle(agency, id, name, order_id, model, **row))
            else:
                low = row['low']
                high = row['high']
                del row['low']
                del row['high']
                for id in range(low, high + 1):
                    if agency.vehicle_name_length:
                        if type(id) is int:
                            name = f'{id:0{agency.vehicle_name_length}d}'
                            id = str(id)
                        else:
                            id = str(id)
                            name = id[:agency.vehicle_name_length]
                    else:
                        id = str(id)
                        name = id
                    vehicles.append(Vehicle(agency, id, name, order_id, model, **row))
        return cls(order_id, agency, model, vehicles)
