
class Region:
    '''A large area that contains multiple systems'''
    
    __slots__ = (
        'id',
        'name'
    )
    
    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.name < other.name
