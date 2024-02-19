
import json

from models.system import System

import helpers.region

systems = {}

def load():
    '''Loads system data from the static JSON file'''
    global systems
    systems = {}
    helpers.region.load()
    with open(f'./static/systems.json', 'r') as file:
        for (region_id, region_values) in json.load(file).items():
            region = helpers.region.find(region_id)
            for (id, values) in region_values.items():
                systems[id] = System(id, region, **values)

def find(system_id):
    '''Returns the system with the given ID'''
    if system_id is not None and system_id in systems:
        return systems[system_id]
    return None

def find_all():
    '''Returns all systems'''
    return systems.values()
