
from dataclasses import dataclass, field

from models.bus import Bus
from models.context import Context
from models.model import Model

@dataclass(slots=True)
class Order:
    '''A range of buses of a specific model ordered in a specific year'''
    
    context: Context
    model: Model
    low: int
    high: int
    year: int | None = None
    visible: bool = True
    demo: bool = False
    exceptions: set[int] = field(default_factory=set)
    
    size: int = field(init=False)
    
    @property
    def first_bus(self):
        '''The first bus in the order'''
        return Bus(self.context, self.low, self)
    
    @property
    def last_bus(self):
        '''The last bus in the order'''
        return Bus(self.context, self.high, self)
    
    def __post_init__(self):
        self.size = (self.high - self.low) + 1 - len(self.exceptions)
    
    def __str__(self):
        model = self.model
        year = self.year
        if model and year:
            return f'{year} {model}'
        return 'Unknown year/model'
    
    def __hash__(self):
        return hash((self.context, self.low, self.high))
    
    def __eq__(self, other):
        return self.context == other.context and self.low == other.low and self.high == other.high
    
    def __lt__(self, other):
        if self.context == other.context:
            return self.low < other.low
        return self.context < other.context
    
    def __iter__(self):
        for number in range(self.low, self.high + 1):
            if number not in self.exceptions:
                yield Bus(self.context, number, self)
    
    def __contains__(self, bus_number):
        if bus_number in self.exceptions:
            return False
        return self.low <= bus_number <= self.high
    
    def previous_bus(self, bus_number):
        '''The previous bus before the given bus number'''
        if bus_number <= self.low:
            return None
        previous_bus_number = bus_number - 1
        if previous_bus_number in self.exceptions:
            return self.previous_bus(previous_bus_number)
        return Bus(self.context, previous_bus_number, self)
    
    def next_bus(self, bus_number):
        '''The next bus following the given bus number'''
        if bus_number >= self.high:
            return None
        next_bus_number = bus_number + 1
        if next_bus_number in self.exceptions:
            return self.next_bus(next_bus_number)
        return Bus(self.context, next_bus_number, self)
