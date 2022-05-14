
import queries.model

class Order:
    '''A range of buses of a specific model ordered in a specific year'''
    
    __slots__ = ('low', 'high', 'year', 'model', 'size')
    
    @classmethod
    def from_csv(cls, row):
        low = int(row['low'])
        high = int(row['high'])
        year = int(row['year'])
        model = queries.model.find(row['model_id'])
        return cls(low, high, year, model)
    
    def __init__(self, low, high, year, model):
        self.low = low
        self.high = high
        self.year = year
        self.model = model
        
        self.size = (self.high - self.low) + 1
    
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
        return range(self.low, self.high + 1)
    
    def contains(self, bus_number):
        return self.low <= bus_number <= self.high
