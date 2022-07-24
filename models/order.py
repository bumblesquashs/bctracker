
import helpers.model

from models.bus import Bus

class Order:
    '''A range of buses of a specific model ordered in a specific year'''
    
    __slots__ = ('low', 'high', 'year', 'model', 'size', 'exceptions')
    
    @classmethod
    def from_csv(cls, row):
        low = int(row['low'])
        high = int(row['high'])
        year = int(row['year'])
        model = helpers.model.find(row['model_id'])
        exceptions = row['exceptions']
        if exceptions == '':
            exceptions = set()
        else:
            exceptions = {int(e) for e in row['exceptions'].split(';')}
        return cls(low, high, year, model, exceptions)
    
    def __init__(self, low, high, year, model, exceptions):
        self.low = low
        self.high = high
        self.year = year
        self.model = model
        self.exceptions = exceptions
        
        self.size = (self.high - self.low) + 1 - len(exceptions)
    
    def __str__(self):
        model = self.model
        if model is None:
            return str(self.year)
        return f'{self.year} {model}'
    
    def __hash__(self):
        return hash((self.low, self.high))
    
    def __eq__(self, other):
        return self.low == other.low and self.high == other.high
    
    def __lt__(self, other):
        return self.low < other.low
    
    @property
    def range(self):
        return (n for n in range(self.low, self.high + 1) if n not in self.exceptions)
    
    @property
    def first_bus(self):
        return Bus(self.low)
    
    @property
    def last_bus(self):
        return Bus(self.high)
    
    def previous_bus(self, bus_number):
        if bus_number <= self.low:
            return None
        previous_bus_number = bus_number - 1
        if previous_bus_number in self.exceptions:
            return self.previous_bus(previous_bus_number)
        return Bus(previous_bus_number)
    
    def next_bus(self, bus_number):
        if bus_number >= self.high:
            return None
        next_bus_number = bus_number + 1
        if next_bus_number in self.exceptions:
            return self.next_bus(next_bus_number)
        return Bus(next_bus_number)
    
    def contains(self, bus_number):
        if bus_number in self.exceptions:
            return False
        return self.low <= bus_number <= self.high
