
import json

from models.adornment import Adornment

adornments = {}

def load():
    '''Loads adornment data from the static JSON file'''
    global adornments
    adornments = {}
    with open(f'./static/adornments.json', 'r') as file:
        for (agency_id, agency_values) in json.load(file).items():
            agency_adornments = {}
            for (bus_number, values) in agency_values.items():
                bus_number = int(bus_number)
                agency_adornments[bus_number] = Adornment(agency_id, bus_number, **values)
            adornments[agency_id] = agency_adornments

def find(agency, bus):
    '''Returns the adornments with the given bus number'''
    agency_id = getattr(agency, 'id', agency)
    bus_number = getattr(bus, 'number', bus)
    if agency_id in adornments:
        agency_adornments = adornments[agency_id]
        if bus_number in agency_adornments:
            return agency_adornments[bus_number]
    return None
