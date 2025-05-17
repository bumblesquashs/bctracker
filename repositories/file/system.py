
import json
import pytz

from di import di

from models.system import System

from repositories import AgencyRepository, RegionRepository, SystemRepository

class FileSystemRepository(SystemRepository):
    
    __slots__ = (
        'agency_repository',
        'region_repository',
        'systems'
    )
    
    def __init__(self, **kwargs):
        self.agency_repository = kwargs.get('agency_repository') or di[AgencyRepository]
        self.region_repository = kwargs.get('region_repository') or di[RegionRepository]
        self.systems = {}
    
    def load(self):
        '''Loads system data from the static JSON file'''
        self.systems = {}
        self.agency_repository.load()
        self.region_repository.load()
        with open(f'./static/systems.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = self.agency_repository.find(agency_id)
                for (region_id, region_values) in agency_values.items():
                    region = self.region_repository.find(region_id)
                    for (id, values) in region_values.items():
                        if not agency.enabled:
                            values['enabled'] = False
                        if 'timezone' in values:
                            values['timezone'] = pytz.timezone(values['timezone'])
                        self.systems[id] = System(id, agency, region, **values)
    
    def find(self, system_id):
        '''Returns the system with the given ID'''
        return self.systems.get(system_id)
    
    def find_all(self, enabled_only: bool = True):
        '''Returns all systems'''
        if enabled_only:
            return [s for s in self.systems.values() if s.enabled]
        return self.systems.values()
