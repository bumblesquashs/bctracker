
import csv

from models.icon import Icon

icons = {}

def load():
    '''Loads icon data from the static CSV file'''
    with open(f'./static/icons.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            icon = Icon.from_csv(dict(zip(columns, row)))
            icons[icon.bus_number] = icon

def find(bus_number):
    '''Returns the icons with the given bus number'''
    if bus_number in icons:
        return icons[bus_number]
    return None

def delete_all():
    '''Deletes all icons'''
    global icons
    icons = {}
