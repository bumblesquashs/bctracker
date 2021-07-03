
from models.bus_order import get_order
import realtime

class Bus:
    def __init__(self, bus_id, number):
        self.id = bus_id
        self.number = number

    def __str__(self):
        if self.number is None:
            return 'Unknown Bus'
        return str(self.number)
    
    def __hash__(self):
        if self.number is None:
            return hash(self.id)
        return hash(self.number)
    
    def __eq__(self, other):
        if self.number is None or other.number is None:
            return self.id == other.id
        return self.number == other.number
    
    def __lt__(self, other):
        self_number = -1 if self.number is None else self.number
        other_number = -1 if other.number is None else other.number
        return self_number < other_number
    
    @property
    def order(self):
        return get_order(self.number)
    
    @property
    def model(self):
        order = self.order
        if order is None:
            return None
        return order.model
    
    @property
    def position(self):
        return realtime.get_position(self.id)
    
    @property
    def json_data(self):
        return {
            'id': self.id,
            'number': str(self),
            'lon': self.position.lon,
            'lat': self.position.lat
        }
