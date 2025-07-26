
from dataclasses import dataclass

@dataclass(slots=True)
class Livery:
    '''The paint scheme for a bus'''
    
    agency_id: str
    id: int
    name: str
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash((self.agency_id, self.id))
    
    def __eq__(self, other):
        return self.agency_id == other.agency_id and self.id == other.id
