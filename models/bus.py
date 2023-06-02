
import helpers.adornment
import helpers.order

class Bus:
    '''A public transportation vehicle'''
    
    __slots__ = ('number', 'order', 'adornment')
    
    def __init__(self, bus_number):
        self.number = bus_number
        self.order = helpers.order.find(bus_number)
        self.adornment = helpers.adornment.find(bus_number)
    
    def __str__(self):
        if self.is_known:
            return f'{self.number:04d}'
        return 'Unknown Bus'
    
    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        return self.number == other.number
    
    def __lt__(self, other):
        return self.number < other.number
    
    @property
    def is_known(self):
        return self.number >= 0
    
    @property
    def model(self):
        '''Returns the model of this bus'''
        order = self.order
        if order is None:
            return None
        return order.model
    
    @property
    def is_test(self):
        model = self.model
        if model is None:
            return False
        return model.is_test
