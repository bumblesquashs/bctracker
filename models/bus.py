
from di import di

from repositories import AdornmentRepository, OrderRepository

class Bus:
    '''A public transportation vehicle'''
    
    __slots__ = (
        'adornment_repository',
        'number',
        'order'
    )
    
    @classmethod
    def find(cls, agency, number, **kwargs):
        '''Returns a bus for the given agency with the given number'''
        order_repository = kwargs.get('order_repository') or di[OrderRepository]
        order = order_repository.find(agency, number)
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
    
    def __init__(self, number, order, **kwargs):
        self.number = number
        self.order = order
        
        self.adornment_repository = kwargs.get('adornment_repository') or di[AdornmentRepository]
    
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
            return self.adornment_repository.find(agency, self)
        return None
