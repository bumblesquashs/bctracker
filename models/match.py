
from dataclasses import dataclass

@dataclass(slots=True)
class Match:
    '''A search result with a value indicating how closely it matches the query'''
    
    name: str
    description: str
    icon: str
    path: str
    value: int
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        if self.value == other.value:
            return self.name < other.name
        return self.value > other.value
    
    def get_json(self, context, get_url):
        '''Returns a representation of this match in JSON-compatible format'''
        return {
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'url': get_url(context, self.path)
        }
