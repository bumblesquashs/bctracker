
import helpers.model

from models.bcf_ferry import BcfFerry

class BcfOrder:
    '''A group of ferries ordered in the same year'''
    
    __slots__ = ('names', 'year_string', 'model')
    
    def __init__(self, names, year_string, model):
        self.names = names
        self.year_string = year_string
        self.model = model
    
    def __str__(self):
        model = self.model
        if model is None:
            return str(self.year_string)
        return f'{self.year_string} {model}'
    
    def __hash__(self):
        return hash(tuple(self.names))
    
    def __eq__(self, other):
        return self.year_string == other.year_string and self.names == other.names
    
    def __lt__(self, other):
        return self.model.name < other.model.name
    
    def __iter__(self):
        for idx in range(len(self.names)):
            yield Bcf_Ferry(self.names[idx], order=self)
    
    @property
    def is_test(self):
        '''Checks if this is a test order'''
        model = self.model
        if model is None:
            return False
        return model.is_test
        
    @property
    def size(self):
        return len(self.names)
    
    @property
    def first_bus(self):
        '''The first ferry in the order'''
        return Bcf_Ferry(self.names[0], order=self)
    
    @property
    def last_bus(self):
        '''The last ferry in the order'''
        return Bcf_Ferry(self.names[-1], order=self)
    
    def previous_bus(self, name):
        '''The previous ferry before the given ferry name'''
        idx = self.names.index(name)
        if idx <= 0:
            return None
        return Bcf_Ferry(self.names[idx - 1], order=self)
    
    def next_bus(self, name):
        '''The next ferry following the given ferry name'''
        idx = self.names.index(name)
        if name >= (self.size - 1):
            return None
        return Bcf_Ferry(self.names[idx + 1], order=self)

    
    def contains(self, name):
        '''Checks if this order contains the given ferry'''
        return name in self.names
