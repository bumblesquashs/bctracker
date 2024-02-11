
import helpers.adornment
import helpers.order

class Bus:
    '''A public transportation vehicle'''
    
    __slots__ = (
        'number',
        'order'
    )
    
    @property
    def is_known(self):
        '''Checks if the bus number is known'''
        return self.number >= 0
    
    @property
    def visible(self):
        '''Checks if the bus is visible'''
        order = self.order
        if order is None:
            return True
        return order.visible
    
    @property
    def model(self):
        '''Returns the model of this bus'''
        order = self.order
        if order is None:
            return None
        return order.model
    
    @classmethod
    def find(cls, agency, number):
        order = helpers.order.find(agency, number)
        return cls(number, order)
    
    def __init__(self, number, order):
        self.number = number
        self.order = order
    
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
    
    def find_adornment(self):
        if self.order is None:
            return None
        return helpers.adornment.find(self.order.agency, self)
