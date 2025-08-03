
from dataclasses import dataclass

@dataclass(slots=True)
class Decoration:
    '''Text placed after a bus number'''
    
    agency_id: str
    vehicle_id: int
    text: str
    description: str | None = None
    enabled: bool = True
    
    def __str__(self):
        return self.text
    
    def __hash__(self):
        return hash((self.agency_id, self.vehicle_id))
    
    def __eq__(self, other):
        return self.agency_id == other.agency_id and self.vehicle_id == other.vehicle_id
