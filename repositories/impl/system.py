
from dataclasses import dataclass, field
import json
import pytz

from models.system import System

import repositories

@dataclass(slots=True)
class SystemRepository:
    
    systems: dict[str, System] = field(default_factory=dict)
    
    def load(self):
        '''Loads system data from the static JSON file'''
        self.systems = {}
        repositories.agency.load()
        repositories.region.load()
        with open(f'./static/systems.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = repositories.agency.find(agency_id)
                for (region_id, region_values) in agency_values.items():
                    region = repositories.region.find(region_id)
                    for (id, values) in region_values.items():
                        if not agency.enabled:
                            values['enabled'] = False
                        if 'timezone' in values:
                            values['timezone'] = pytz.timezone(values['timezone'])
                        self.systems[id] = System(id, agency, region, **values)
    
    def find(self, system_id) -> System | None:
        '''Returns the system with the given ID'''
        return self.systems.get(system_id)
    
    def find_all(self, enabled_only: bool = True) -> list[System]:
        '''Returns all systems'''
        if enabled_only:
            return [s for s in self.systems.values() if s.enabled]
        return self.systems.values()
