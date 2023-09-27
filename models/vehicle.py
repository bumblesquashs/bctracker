
import helpers.adornment
import helpers.order

class Vehicle:
    '''A public transportation vehicle capable of being tracked'''
    
    __slots__ = ('id', 'order', 'adornment', 'is_named')
    
    def __init__(self, id, order=None, adornment=None, is_named=False):
        self.id = id
        self.is_named = is_named # Whether to use fleet numbers or names
        if order is None:
            self.order = helpers.order.find(id, is_named)
        else:
            self.order = order
        if adornment is None:
            self.adornment = helpers.adornment.find(id)
        else:
            self.adornment = adornment
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
        
    def __str__(self):
        return self.id
        
    @property
    def model(self):
        if self.order is None:
            return None
        return self.order.model
    
    
    @property
    def is_test(self):
        '''Checks if this is a test vehicle'''
        if self.order is None:
            return False
        return self.order.is_test
        
    @property
    def is_known(self):
        '''Checks if the vehicle is known'''
        return True
            
