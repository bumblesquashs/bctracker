
import json

from models.system import System

import helpers.agency
import helpers.region

class SystemService:
    
    __slots__ = (
        'systems'
    )
    
    def __init__(self):
        self.systems = {}
    
    def load(self):
        '''Loads system data from the static JSON file'''
        self.systems = {}
        helpers.agency.default.load()
        helpers.region.default.load()
        with open(f'./static/systems.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = helpers.agency.default.find(agency_id)
                for (region_id, region_values) in agency_values.items():
                    region = helpers.region.default.find(region_id)
                    for (id, values) in region_values.items():
                        self.systems[id] = System(id, agency, region, **values)
    
    def find(self, system_id):
        '''Returns the system with the given ID'''
        return self.systems.get(system_id)
    
    def find_all(self):
        '''Returns all systems'''
        return self.systems.values()

default = SystemService()
