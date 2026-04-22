
from dataclasses import dataclass, field
import json

from models.theme import Theme

@dataclass(slots=True)
class ThemeRepository:
    
    themes: dict[str, Theme] = field(default_factory=dict)
    
    def load(self):
        '''Loads theme data from the static JSON file'''
        self.themes = {}
        with open(f'./static/themes.json', 'r') as file:
            for (id, values) in json.load(file).items():
                self.themes[id] = Theme(id, **values)
    
    def find(self, theme_id: str) -> Theme | None:
        '''Returns the theme with the given ID'''
        return self.themes.get(theme_id)
    
    def find_all(self) -> list[Theme]:
        '''Returns all themes'''
        return self.themes.values()
