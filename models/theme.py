
from dataclasses import dataclass

@dataclass(slots=True)
class Theme:
    '''A set of CSS styles that feature different colours'''
    
    id: str
    name: str
    visible: bool = True
    light: bool = False
    dark: bool = False
    show_header_curve: bool = False
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
