
from dataclasses import dataclass

@dataclass(slots=True)
class Region:
    '''A large area that contains multiple systems'''
    
    id: str
    name: str
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.name < other.name
