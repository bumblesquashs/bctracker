
from dataclasses import dataclass, field
import json

from models.livery import Livery

@dataclass(slots=True)
class LiveryRepository:
    
    liveries: dict[str, dict[str, Livery]] = field(default_factory=dict)
    
    def load(self):
        '''Loads decoration data from the static JSON file'''
        self.liveries = {}
        with open(f'./static/liveries.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency_liveries = {}
                for (id, values) in agency_values.items():
                    agency_liveries[id] = Livery(agency_id, id, **values)
                self.liveries[agency_id] = agency_liveries
    
    def find(self, agency_id: str, id: str) -> Livery | None:
        '''Returns the livery with the given ID'''
        try:
            return self.liveries[agency_id][id]
        except KeyError:
            return None
