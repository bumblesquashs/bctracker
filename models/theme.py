
class Theme:
    '''A set of CSS styles that feature different colours'''
    
    __slots__ = ('id', 'name', 'map_style', 'visible')
    
    @classmethod
    def from_csv(cls, row):
        '''Returns a theme initialized from the given CSV row'''
        id = row['id']
        name = row['name']
        map_style = row['map_style']
        visible = row['visible'] == '1'
        return cls(id, name, map_style, visible)
    
    def __init__(self, id, name, map_style, visible):
        self.id = id
        self.name = name
        self.map_style = map_style
        self.visible = visible
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
