
import csv

from models.theme import Theme

themes = {}

def load():
    '''Loads theme data from the static CSV file'''
    with open(f'./data/static/themes.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            theme = Theme.from_csv(dict(zip(columns, row)))
            themes[theme.id] = theme

def find(theme_id):
    '''Returns the theme with the given ID'''
    if theme_id is not None and theme_id in themes:
        return themes[theme_id]
    return None

def find_all():
    '''Returns all themes'''
    return themes.values()
