
from dataclasses import dataclass, field
import json

from models.adornment import Adornment

@dataclass(slots=True)
class AdornmentRepository:
    
    adornments: dict[str, dict[int, Adornment]] = field(default_factory=dict)
    
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
    
    def find(self, bus) -> Adornment | None:
        '''Returns the adornments with the given bus number'''
        try:
            return self.adornments[bus.context.agency_id][bus.number]
        except KeyError:
            return None
