
from dataclasses import dataclass

@dataclass(slots=True)
class Adornment:
    '''Text placed after a bus number'''
    
    agency_id: str
    bus_number: int
    text: str
    description: str | None = None
    enabled: bool = True
    
    def __str__(self):
        return self.text
    
    def __hash__(self):
        return hash((self.agency_id, self.bus_number))
    
    def __eq__(self, other):
        return self.agency_id == other.agency_id and self.bus_number == other.bus_number
