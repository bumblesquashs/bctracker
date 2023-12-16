
class Adornment:
    '''Text placed after a bus number'''
    
    __slots__ = (
        'bus_number',
        'enabled',
        'text',
        'description'
    )
    
    @classmethod
    def from_csv(cls, row):
        '''Returns an adornment initialized from the given CSV row'''
        bus_number = int(row['bus_number'])
        enabled = row['enabled'] == '1'
        text = row['text']
        if row['description'] == '':
            description = None
        else:
            description = row['description']
        return cls(bus_number, enabled, text, description)
    
    def __init__(self, bus_number, enabled, text, description):
        self.bus_number = bus_number
        self.enabled = enabled
        self.text = text
        self.description = description
    
    def __str__(self):
        return self.text
    
    def __hash__(self):
        return hash(self.bus_number)
    
    def __eq__(self, other):
        return self.bus_number == other.bus_number
