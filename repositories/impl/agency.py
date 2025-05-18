
import json

from models.agency import Agency

class AgencyRepository:
    
    __slots__ = (
        'agencies'
    )
    
    def __init__(self):
        self.agencies = {}
    
    def load(self):
        '''Loads agency data from the static JSON file'''
        self.agencies = {}
        with open(f'./static/agencies.json', 'r') as file:
            for (id, values) in json.load(file).items():
                self.agencies[id] = Agency(id, **values)
    
    def find(self, agency_id):
        '''Returns the agency with the given ID'''
        return self.agencies.get(agency_id)
    
    def find_all(self, enabled_only: bool = True):
        '''Returns all agencies'''
        if enabled_only:
            return sorted([a for a in self.agencies.values() if a.enabled])
        return sorted(self.agencies.values())
