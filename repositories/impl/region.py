
from dataclasses import dataclass, field
import json

from models.region import Region

@dataclass(slots=True)
class RegionRepository:
    
    regions: dict[str, Region] = field(default_factory=dict)
    
    def load(self):
        '''Loads region data from the static JSON file'''
        self.regions = {}
        with open(f'./static/regions.json', 'r') as file:
            for (id, values) in json.load(file).items():
                self.regions[id] = Region(id, **values)
    
    def find(self, region_id: str) -> Region | None:
        '''Returns the region with the given ID'''
        return self.regions.get(region_id)
    
    def find_all(self) -> list[Region]:
        '''Returns all regions'''
        return self.regions.values()
