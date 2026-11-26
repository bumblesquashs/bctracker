
from dataclasses import dataclass, field
from glob import glob
import json

from models.livery import Livery

import settings

@dataclass(slots=True)
class LiveryRepository:
    
    liveries: dict[str, dict[str, Livery]] = field(default_factory=dict)
    
    def load(self):
        '''Loads decoration data from the static JSON file'''
        self.liveries = {}
        root_path = f'./config/{settings.current.province.path_id}/agencies'
        file_name = 'liveries.json'
        agency_paths = glob(f'{root_path}/*/{file_name}')
        for path in agency_paths:
            with open(path, 'r') as file:
                values = json.load(file)
            agency_id = path[len(root_path):-len(file_name)].strip('/')
            self.liveries[agency_id] = {k: Livery(agency_id, k, **v) for k, v in values.items()}
    
    def find(self, agency_id: str, id: str) -> Livery | None:
        '''Returns the livery with the given ID'''
        try:
            return self.liveries[agency_id][id]
        except KeyError:
            return None
