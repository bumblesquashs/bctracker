
from dataclasses import dataclass, field
import json

from models.decoration import Decoration

@dataclass(slots=True)
class DecorationRepository:
    
    decorations: dict[str, dict[int, Decoration]] = field(default_factory=dict)
    
    def load(self):
        '''Loads decoration data from the static JSON file'''
        self.decorations = {}
        with open(f'./static/decorations.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency_decorations = {}
                for (bus_number, values) in agency_values.items():
                    agency_decorations[bus_number] = Decoration(agency_id, bus_number, **values)
                self.decorations[agency_id] = agency_decorations
    
    def find(self, bus) -> Decoration | None:
        '''Returns the decorations with the given bus number'''
        try:
            return self.decorations[bus.context.agency_id][bus.number]
        except KeyError:
            return None
