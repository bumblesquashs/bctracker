
class Adornment:
    '''Text placed after a bus number'''
    
    __slots__ = (
        'bus_number',
        'text',
        'description',
        'enabled'
    )
    
    def __init__(self, bus_number, text, description=None, enabled=True):
        self.bus_number = bus_number
        self.text = text
        self.description = description
        self.enabled = enabled
    
    def __str__(self):
        return self.text
    
    def __hash__(self):
        return hash(self.bus_number)
    
    def __eq__(self, other):
        return self.bus_number == other.bus_number
