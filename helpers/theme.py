
import json

from models.theme import Theme

class ThemeService:
    
    __slots__ = (
        'themes'
    )
    
    def __init__(self):
        self.themes = {}
    
    def load(self):
        '''Loads theme data from the static JSON file'''
        self.themes = {}
        with open(f'./static/themes.json', 'r') as file:
            for (id, values) in json.load(file).items():
                self.themes[id] = Theme(id, **values)
    
    def find(self, theme_id):
        '''Returns the theme with the given ID'''
        return self.themes.get(theme_id)
    
    def find_all(self):
        '''Returns all themes'''
        return self.themes.values()
