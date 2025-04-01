
from models.bus import Bus

class Order:
    '''A range of buses of a specific model ordered in a specific year'''
    
    __slots__ = (
        'agency',
        'model',
        'prefix',
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
        return Bus(self.agency, self.with_prefix(self.low), self)
    
    @property
    def last_bus(self):
        '''The last bus in the order'''
        return Bus(self.agency, self.with_prefix(self.high), self)
    
    def __init__(self, agency, model, **kwargs):
        self.agency = agency
        self.model = model
        self.prefix = kwargs.get('prefix')
        if 'number' in kwargs:
            self.low = kwargs['number']
            self.high = kwargs['number']
        else:
            self.low = kwargs['low']
            self.high = kwargs['high']
        self.year = kwargs.get('year')
        self.visible = kwargs.get('visible', True)
        self.demo = kwargs.get('demo', False)
        if 'exceptions' in kwargs:
            self.exceptions = set(kwargs['exceptions'])
        else:
            self.exceptions = set()
        
        self.size = (self.high - self.low) + 1 - len(self.exceptions)
    
    def __str__(self):
        model = self.model
        year = self.year
        if model and year:
            return f'{year} {model}'
        return 'Unknown year/model'
    
    def __hash__(self):
        return hash((self.agency, self.prefix, self.low, self.high))
    
    def __eq__(self, other):
        return self.agency == other.agency and self.prefix == other.prefix and self.low == other.low and self.high == other.high
    
    def __lt__(self, other):
        if self.agency == other.agency:
            if self.prefix and other.prefix and self.prefix != other.prefix:
                return self.prefix < other.prefix
            if self.prefix and not other.prefix:
                return False
            if not self.prefix and other.prefix:
                return True
            return self.low < other.low
        return self.agency < other.agency
    
    def __iter__(self):
        for number in range(self.low, self.high + 1):
            if number not in self.exceptions:
                yield Bus(self.agency, self.with_prefix(number), self)
    
    def __contains__(self, bus_number):
        if self.prefix and not bus_number.startswith(self.prefix):
            return False
        if not self.prefix and len([c for c in bus_number if not c.isdigit()]) > 0:
            return False
        number = self.without_prefix(bus_number)
        if number in self.exceptions:
            return False
        return self.low <= number <= self.high
    
    def previous_bus(self, bus_number):
        '''The previous bus before the given bus number'''
        number = self.without_prefix(bus_number)
        if number <= self.low:
            return None
        previous_bus_number = number - 1
        if previous_bus_number in self.exceptions:
            return self.previous_bus(previous_bus_number)
        return Bus(self.agency, self.with_prefix(previous_bus_number), self)
    
    def next_bus(self, bus_number):
        '''The next bus following the given bus number'''
        number = self.without_prefix(bus_number)
        if number >= self.high:
            return None
        next_bus_number = number + 1
        if next_bus_number in self.exceptions:
            return self.next_bus(next_bus_number)
        return Bus(self.agency, self.with_prefix(next_bus_number), self)
    
    def with_prefix(self, number):
        if self.prefix:
            return f'{self.prefix}{number}'
        return str(number)
    
    def without_prefix(self, number):
        if self.prefix:
            return int(number[len(self.prefix):])
        return int(''.join(c for c in number if c.isdigit()))
