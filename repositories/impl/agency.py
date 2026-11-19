
from dataclasses import dataclass, field
from glob import glob
import json

from models.agency import Agency

import settings

@dataclass(slots=True)
class AgencyRepository:
    
    agencies: dict[str, Agency] = field(default_factory=dict)
    
    def load(self):
        '''Loads agency data from the static JSON file'''
        self.agencies = {}
        root_path = f'./config/{settings.current.province.path_id}/agencies'
        file_name = 'agency.json'
        agency_paths = glob(f'{root_path}/*/{file_name}')
        for path in agency_paths:
            with open(path, 'r') as file:
                values = json.load(file)
            agency_id = path[len(root_path):-len(file_name)].strip('/')
            self.agencies[agency_id] = Agency(agency_id, **values)
    
    def find(self, agency_id: str) -> Agency | None:
        '''Returns the agency with the given ID'''
        return self.agencies.get(agency_id)
    
    def find_all(self, enabled_only: bool = True) -> list[Agency]:
        '''Returns all agencies'''
        if enabled_only:
            return sorted([a for a in self.agencies.values() if a.enabled])
        return sorted(self.agencies.values())
