
from dataclasses import dataclass, field

from models.agency import Agency
from models.bus import Bus
from models.model import Model

@dataclass(slots=True)
class Order:
    '''A set of buses of a specific model'''
    
    id: int
    agency: Agency
    model: Model | None
    buses: list[Bus]
    
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
        self.key = min([b.key for b in self.buses])
        self.years = sorted({b.year for b in self.buses})
        self.visible = any(b.visible for b in self.buses)
    
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
    
    def previous_bus(self, bus):
        '''The previous bus before the given bus'''
        try:
            index = self.buses.index(bus)
            return self.buses[index - 1]
        except (IndexError, ValueError):
            return None
    
    def next_bus(self, bus):
        '''The next bus following the given bus'''
        try:
            index = self.buses.index(bus)
            return self.buses[index + 1]
        except (IndexError, ValueError):
            return None
    
    @classmethod
    def from_json(cls, id: int, agency: Agency, model: Model | None, rows: list):
        buses = []
        for row in rows:
            if 'number' in row:
                number = row['number']
                del row['number']
                if agency.vehicle_name_length:
                    if type(number) is int:
                        name = f'{number:0{agency.vehicle_name_length}d}'
                        number = str(number)
                    else:
                        number = str(number)
                        name = number[:agency.vehicle_name_length]
                else:
                    number = str(number)
                    name = number
                buses.append(Bus(agency, number, name, id, model, **row))
            else:
                low = row['low']
                high = row['high']
                del row['low']
                del row['high']
                for number in range(low, high + 1):
                    if agency.vehicle_name_length:
                        if type(number) is int:
                            name = f'{number:0{agency.vehicle_name_length}d}'
                            number = str(number)
                        else:
                            number = str(number)
                            name = number[:agency.vehicle_name_length]
                    else:
                        number = str(number)
                        name = number
                    buses.append(Bus(agency, number, name, id, model, **row))
        return cls(id, agency, model, buses)
