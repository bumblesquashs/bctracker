
from di import di

from services import AdornmentService, OrderService

class Bus:
    '''A public transportation vehicle'''
    
    __slots__ = (
        'number',
        'order'
    )
    
    @classmethod
    def find(cls, agency, number):
        '''Returns a bus for the given agency with the given number'''
        order = di[OrderService].find(agency, number)
        return cls(number, order)
    
    @property
    def is_known(self):
        '''Checks if the bus number is known'''
        return self.number >= 0
    
    @property
    def visible(self):
        '''Checks if the bus is visible'''
        order = self.order
        if order:
            return order.visible
        return True
    
    @property
    def model(self):
        '''Returns the model of this bus'''
        order = self.order
        if order:
            return order.model
        return None
    
    @property
    def agency(self):
        order = self.order
        if order:
            return order.agency
        return None
    
    def __init__(self, number, order):
        self.number = number
        self.order = order
    
    def __str__(self):
        if self.is_known:
            agency = self.agency
            if agency and agency.vehicle_name_length:
                return f'{self.number:0{agency.vehicle_name_length}d}'
            return str(self.number)
        return 'Unknown Bus'
    
    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        return self.number == other.number
    
    def __lt__(self, other):
        return self.number < other.number
    
    def find_adornment(self):
        '''Returns the adornment for this bus, if one exists'''
        agency = self.agency
        if agency:
            return di[AdornmentService].find(agency, self)
        return None
