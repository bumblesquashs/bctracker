
import json

from models.theme import Theme

themes = {}

def load():
    '''Loads theme data from the static JSON file'''
    global themes
    themes = {}
    with open(f'./static/themes.json', 'r') as file:
        for (id, values) in json.load(file).items():
            themes[id] = Theme(id, **values)

def find(theme_id):
    '''Returns the theme with the given ID'''
    try:
        return themes[theme_id]
    except KeyError:
        return None

def find_all():
    '''Returns all themes'''
    return themes.values()
