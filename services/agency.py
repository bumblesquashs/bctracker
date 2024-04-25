
import json

from models.agency import Agency

from services import AgencyService

class DefaultAgencyService(AgencyService):
    
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
    
    def find_all(self):
        '''Returns all agencies'''
        return self.agencies.values()
