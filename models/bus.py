
from models.order import get_order

class Bus:
    __slots__ = ('number', 'order')
    
    def __init__(self, bus_number):
        self.number = bus_number
        self.order = get_order(bus_number)
    
    def __str__(self):
        if self.number < 0:
            return 'Unknown Bus'
        return str(self.number)
    
    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        return self.number == other.number
    
    def __lt__(self, other):
        return self.number < other.number
    
    @property
    def model(self):
        order = self.order
        if order is None:
            return None
        return order.model
