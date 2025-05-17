
from di import di

from models.context import Context

from repositories import AdornmentRepository, OrderRepository

class Bus:
    '''A public transportation vehicle'''
    
    __slots__ = (
        'adornment_repository',
        'context',
        'number',
        'order'
    )
    
    @classmethod
    def find(cls, context: Context, number, **kwargs):
        '''Returns a bus for the given context with the given number'''
        order_repository = kwargs.get('order_repository') or di[OrderRepository]
        order = order_repository.find(context, number)
        return cls(context, number, order)
    
    @property
    def url_id(self):
        '''The ID to use when making bus URLs'''
        return self.number
    
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
    
    def __init__(self, context: Context, number, order, **kwargs):
        self.context = context
        self.number = number
        self.order = order
        
        self.adornment_repository = kwargs.get('adornment_repository') or di[AdornmentRepository]
    
    def __str__(self):
        if self.is_known:
            if self.context.vehicle_name_length:
                return f'{self.number:0{self.context.vehicle_name_length}d}'
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
        return self.adornment_repository.find(self)
