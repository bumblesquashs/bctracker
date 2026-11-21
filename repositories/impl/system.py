
from dataclasses import dataclass, field
from glob import glob
import json
from zoneinfo import ZoneInfo

from models.system import System

import repositories
import settings

@dataclass(slots=True)
class SystemRepository:
    
    systems: dict[str, System] = field(default_factory=dict)
    
    def load(self):
        '''Loads system data from the static JSON file'''
        self.systems = {}
        repositories.agency.load()
        repositories.region.load()
        root_path = f'./config/{settings.current.province.path_id}/agencies'
        file_name = 'systems.json'
        agency_paths = glob(f'{root_path}/*/{file_name}')
        for path in agency_paths:
            with open(path, 'r') as file:
                values = json.load(file)
            agency_id = path[len(root_path):-len(file_name)].strip('/')
            agency = repositories.agency.find(agency_id)
            for (system_id, system_values) in values.items():
                if not agency.enabled:
                    system_values['enabled'] = False
                if 'region' in system_values:
                    system_values['region'] = repositories.region.find(system_values['region'])
                if 'timezone' in system_values:
                    system_values['timezone'] = ZoneInfo(system_values['timezone'])
                self.systems[system_id] = System(system_id, agency, **system_values)
    
    def find(self, system_id: str) -> System | None:
        '''Returns the system with the given ID'''
        return self.systems.get(system_id)
    
    def find_all(self, enabled_only: bool = True) -> list[System]:
        '''Returns all systems'''
        if enabled_only:
            return [s for s in self.systems.values() if s.enabled]
        return self.systems.values()
