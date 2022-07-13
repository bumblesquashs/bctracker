
import csv

from models.theme import Theme

themes = {}

def load():
    with open(f'./data/static/themes.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            theme = Theme.from_csv(dict(zip(columns, row)))
            themes[theme.id] = theme

def find(theme_id):
    if theme_id is not None and theme_id in themes:
        return themes[theme_id]
    return None

def find_all():
    return themes.values()
