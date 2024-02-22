
import helpers.adornment
import helpers.order

class Bus:
    '''A public transportation vehicle'''
    
    __slots__ = (
        'number',
        'order'
    )
    
    @classmethod
    def find(cls, agency, number):
        '''Returns a bus for the given agency with the given number'''
        order = helpers.order.find(agency, number)
        return cls(number, order)
    
    @property
    def is_known(self):
        '''Checks if the bus number is known'''
        return self.number >= 0
    
    @property
    def visible(self):
        '''Checks if the bus is visible'''
        try:
            return self.order.visible
        except AttributeError:
            return True
    
    @property
    def model(self):
        '''Returns the model of this bus'''
        try:
            return self.order.model
        except AttributeError:
            return None
    
    def __init__(self, number, order):
        self.number = number
        self.order = order
    
    def __str__(self):
        if self.is_known:
            try:
                return f'{self.number:0{self.order.agency.vehicle_name_length}d}'
            except AttributeError:
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
        try:
            return helpers.adornment.find(self.order.agency, self)
        except AttributeError:
            return None
