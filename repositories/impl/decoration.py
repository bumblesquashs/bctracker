
from dataclasses import dataclass, field
from glob import glob
import json

from models.decoration import Decoration

import settings

@dataclass(slots=True)
class DecorationRepository:
    
    decorations: dict[str, dict[str, Decoration]] = field(default_factory=dict)
    
    def load(self):
        '''Loads decoration data from the static JSON file'''
        self.decorations = {}
        root_path = f'./config/{settings.current.province.path_id}/agencies'
        file_name = 'decorations.json'
        agency_paths = glob(f'{root_path}/*/{file_name}')
        for path in agency_paths:
            with open(path, 'r') as file:
                values = json.load(file)
            agency_id = path[len(root_path):-len(file_name)].strip('/')
            self.decorations[agency_id] = {k: Decoration(agency_id, k, **v) for k, v in values.items()}
    
    def find(self, agency_id: str, vehicle_id: str) -> Decoration | None:
        '''Returns the decorations with the given vehicle ID'''
        try:
            return self.decorations[agency_id][vehicle_id]
        except KeyError:
            return None
