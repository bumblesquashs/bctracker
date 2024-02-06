
from models.bus import Bus

class Order:
    '''A range of buses of a specific model ordered in a specific year'''
    
    __slots__ = (
        'model',
        'low',
        'high',
        'year',
        'visible',
        'demo',
        'exceptions',
        'size'
    )
    
    @property
    def first_bus(self):
        '''The first bus in the order'''
        return Bus(self.low, order=self)
    
    @property
    def last_bus(self):
        '''The last bus in the order'''
        return Bus(self.high, order=self)
    
    def __init__(self, model, number=None, low=None, high=None, year=None, visible=True, demo=False, exceptions=None):
        self.model = model
        if number is None:
            self.low = low
            self.high = high
        else:
            self.low = number
            self.high = number
        self.year = year
        self.visible = visible
        self.demo = demo
        if exceptions:
            self.exceptions = set(exceptions)
        else:
            self.exceptions = set()
        
        self.size = (self.high - self.low) + 1 - len(self.exceptions)
    
    def __str__(self):
        model = self.model
        year = self.year
        if model is None or year is None:
            return 'Unknown year/model'
        return f'{year} {model}'
    
    def __hash__(self):
        return hash((self.low, self.high))
    
    def __eq__(self, other):
        return self.low == other.low and self.high == other.high
    
    def __lt__(self, other):
        return self.low < other.low
    
    def __iter__(self):
        for number in range(self.low, self.high + 1):
            if number not in self.exceptions:
                yield Bus(number, order=self)
    
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
        return Bus(previous_bus_number, order=self)
    
    def next_bus(self, bus_number):
        '''The next bus following the given bus number'''
        if bus_number >= self.high:
            return None
        next_bus_number = bus_number + 1
        if next_bus_number in self.exceptions:
            return self.next_bus(next_bus_number)
        return Bus(next_bus_number, order=self)
