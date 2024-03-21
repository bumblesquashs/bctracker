
import json

from models.system import System

import helpers.agency
import helpers.region

systems = {}

def load():
    '''Loads system data from the static JSON file'''
    global systems
    systems = {}
    helpers.agency.load()
    helpers.region.load()
    with open(f'./static/systems.json', 'r') as file:
        for (agency_id, agency_values) in json.load(file).items():
            agency = helpers.agency.find(agency_id)
            for (region_id, region_values) in agency_values.items():
                region = helpers.region.find(region_id)
                for (id, values) in region_values.items():
                    systems[id] = System(id, agency, region, **values)

def find(system_id):
    '''Returns the system with the given ID'''
    if system_id is not None and system_id in systems:
        return systems[system_id]
    return None

def find_all(af_2024=False):
    '''Returns all systems'''
    if af_2024:
        return systems.values()
    return [s for s in systems.values() if s.agency.id == 'bc-transit']
