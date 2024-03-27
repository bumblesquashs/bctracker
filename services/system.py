
import json

from di import di

from models.system import System

from services.agency import AgencyService
from services.region import RegionService

class SystemService:
    
    __slots__ = (
        'agency_service',
        'region_service',
        'systems'
    )
    
    def __init__(self, agency_service=di[AgencyService], region_service=di[RegionService]):
        self.agency_service = agency_service
        self.region_service = region_service
        self.systems = {}
    
    def load(self):
        '''Loads system data from the static JSON file'''
        self.systems = {}
        self.agency_service.load()
        self.region_service.load()
        with open(f'./static/systems.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = self.agency_service.find(agency_id)
                for (region_id, region_values) in agency_values.items():
                    region = self.region_service.find(region_id)
                    for (id, values) in region_values.items():
                        self.systems[id] = System(id, agency, region, **values)
    
    def find(self, system_id):
        '''Returns the system with the given ID'''
        try:
            return self.systems[system_id]
        except KeyError:
            return None
    
    def find_all(self):
        '''Returns all systems'''
        return self.systems.values()
