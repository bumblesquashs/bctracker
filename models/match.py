
class Match:
    '''A search result with a value indicating how closely it matches the query'''
    
    __slots__ = ('type', 'name', 'description', 'path', 'value')
    
    def __init__(self, type, name, description, path, value):
        self.type = type
        self.name = name
        self.description = description
        self.path = path
        self.value = value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        if self.value == other.value:
            return self.name < other.name
        return self.value > other.value
    
    def get_json(self, system, get_url):
        '''Returns a representation of this match in JSON-compatible format'''
        return {
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'url': get_url(system, self.path)
        }
