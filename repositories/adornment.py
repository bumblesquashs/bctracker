
import json

from models.adornment import Adornment

from repositories import AdornmentRepository

class DefaultAdornmentRepository(AdornmentRepository):
    
    __slots__ = (
        'adornments'
    )
    
    def __init__(self):
        self.adornments = {}
    
    def load(self):
        '''Loads adornment data from the static JSON file'''
        self.adornments = {}
        with open(f'./static/adornments.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency_adornments = {}
                for (bus_number, values) in agency_values.items():
                    bus_number = int(bus_number)
                    agency_adornments[bus_number] = Adornment(agency_id, bus_number, **values)
                self.adornments[agency_id] = agency_adornments
    
    def find(self, agency, bus):
        '''Returns the adornments with the given bus number'''
        agency_id = getattr(agency, 'id', agency)
        bus_number = getattr(bus, 'number', bus)
        try:
            return self.adornments[agency_id][bus_number]
        except KeyError:
            return None
