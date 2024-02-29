
class Theme:
    '''A set of CSS styles that feature different colours'''
    
    __slots__ = (
        'id',
        'name',
        'light',
        'dark',
        'visible'
    )
    
    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.light = kwargs.get('light', False)
        self.dark = kwargs.get('dark', False)
        self.visible = kwargs.get('visible', True)
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
