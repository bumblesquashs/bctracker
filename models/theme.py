
class Theme:
    '''A set of CSS styles that feature different colours'''
    
    __slots__ = (
        'id',
        'name',
        'visible'
    )
    
    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.visible = kwargs.get('visible', True)
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
