
import helpers.adornment
import helpers.order
from models.vehicle import Vehicle

class Bus(Vehicle):
    '''A bus with ranges/orders'''
    
    __slots__ = ()
    
    def __init__(self, number, order=None, adornment=None):
        super().__init__(id=str(number), order=order, adornment=adornment, is_named=False)
    
    @property
    def number(self):
        return int(self.id)
    
    def __str__(self):
        if self.is_known:
            return f'{self.number:04d}'
        return 'Unknown Bus'
    
    
    def __lt__(self, other):
        return self.number < other.number
    
    @property
    def is_known(self):
        '''Checks if the bus number is known'''
        return self.number >= 0
