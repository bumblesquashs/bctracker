
class Theme:
    '''A set of CSS styles that feature different colours'''
    
    __slots__ = (
        'id',
        'name',
        'visible',
        'light',
        'dark'
    )
    
    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.visible = kwargs.get('visible', True)
        self.light = kwargs.get('light', False)
        self.dark = kwargs.get('dark', False)
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
