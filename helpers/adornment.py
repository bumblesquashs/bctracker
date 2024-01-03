
import csv

from models.adornment import Adornment

adornments = {}

def load():
    '''Loads adornment data from the static CSV file'''
    with open(f'./static/adornments.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            adornment = Adornment.from_csv(dict(zip(columns, row)))
            adornments[adornment.bus_number] = adornment

def find(bus):
    '''Returns the adornments with the given bus number'''
    bus_number = getattr(bus, 'number', bus)
    if bus_number in adornments:
        return adornments[bus_number]
    return None

def delete_all():
    '''Deletes all adornments'''
    global adornments
    adornments = {}
