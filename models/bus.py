
import models.bus_range as bus_range

class Bus:
    def __init__(self, bus_id, number):
        self.id = bus_id
        self.number = number
        self.current_system = None

        self.bus_range = bus_range.get(number)

    def __str__(self):
        if self.number < 0:
            return "Unknown"
        return str(self.number)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.number < other.number
