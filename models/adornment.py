
class Adornment:
    '''Text placed after a bus number'''
    
    __slots__ = (
        'agency_id',
        'bus_number',
        'text',
        'description',
        'enabled'
    )
    
    def __init__(self, agency_id, bus_number, text, description=None, enabled=True):
        self.agency_id = agency_id
        self.bus_number = bus_number
        self.text = text
        self.description = description
        self.enabled = enabled
    
    def __str__(self):
        return self.text
    
    def __hash__(self):
        return hash((self.agency_id, self.bus_number))
    
    def __eq__(self, other):
        return self.agency_id == other.agency_id and self.bus_number == other.bus_number
