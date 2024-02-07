
import json

from models.adornment import Adornment

adornments = {}

def load():
    '''Loads adornment data from the static JSON file'''
    global adornments
    adornments = {}
    with open(f'./static/adornments.json', 'r') as file:
        for (bus_number, values) in json.load(file).items():
            bus_number = int(bus_number)
            adornments[bus_number] = Adornment(bus_number, **values)

def find(bus):
    '''Returns the adornments with the given bus number'''
    bus_number = getattr(bus, 'number', bus)
    if bus_number in adornments:
        return adornments[bus_number]
    return None
