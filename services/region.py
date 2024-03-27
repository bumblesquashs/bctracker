
import json

from models.region import Region

class RegionService:
    
    __slots__ = (
        'regions'
    )
    
    def __init__(self):
        self.regions = {}
    
    def load(self):
        '''Loads region data from the static JSON file'''
        self.regions = {}
        with open(f'./static/regions.json', 'r') as file:
            for (id, values) in json.load(file).items():
                self.regions[id] = Region(id, **values)
    
    def find(self, region_id):
        '''Returns the region with the given ID'''
        try:
            return self.regions[region_id]
        except KeyError:
            return None
    
    def find_all(self):
        '''Returns all regions'''
        return self.regions.values()
