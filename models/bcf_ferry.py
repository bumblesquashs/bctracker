
import helpers.adornment
import helpers.order
from models.vehicle import Vehicle

class BcfFerry(Vehicle):
    '''A vessel from bc_ferries'''
    
    __slots__ = ()
    
    def __init__(self, name, order, adornment=None):
        super().__init__(id=name, order=order, adornment=adornment, is_named=True)
    
    @property
    def is_known(self):
        '''Checks if the ferry is known'''
        return True