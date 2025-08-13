
from dataclasses import dataclass, field
import json

from models.agency import Agency

@dataclass(slots=True)
class AgencyRepository:
    
    agencies: dict[str, Agency] = field(default_factory=dict)
    
    def load(self):
        '''Loads agency data from the static JSON file'''
        self.agencies = {}
        with open(f'./static/agencies.json', 'r') as file:
            for (id, values) in json.load(file).items():
                self.agencies[id] = Agency(id, **values)
    
    def find(self, agency_id: str) -> Agency | None:
        '''Returns the agency with the given ID'''
        return self.agencies.get(agency_id)
    
    def find_all(self, enabled_only: bool = True) -> list[Agency]:
        '''Returns all agencies'''
        if enabled_only:
            return sorted([a for a in self.agencies.values() if a.enabled])
        return sorted(self.agencies.values())
