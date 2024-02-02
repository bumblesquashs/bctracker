
class Theme:
    '''A set of CSS styles that feature different colours'''
    
    __slots__ = (
        'id',
        'name',
        'visible'
    )
    
    @classmethod
    def from_csv(cls, row):
        '''Returns a theme initialized from the given CSV row'''
        id = row['id']
        name = row['name']
        visible = row['visible'] == '1'
        return cls(id, name, visible)
    
    def __init__(self, id, name, visible):
        self.id = id
        self.name = name
        self.visible = visible
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
