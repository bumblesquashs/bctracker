
from dataclasses import dataclass, field
import json

from models.decoration import Decoration

@dataclass(slots=True)
class DecorationRepository:
    
    decorations: dict[str, dict[str, Decoration]] = field(default_factory=dict)
    
    def load(self):
        '''Loads decoration data from the static JSON file'''
        self.decorations = {}
        with open(f'./static/decorations.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency_decorations = {}
                for (vehicle_id, values) in agency_values.items():
                    agency_decorations[vehicle_id] = Decoration(agency_id, vehicle_id, **values)
                self.decorations[agency_id] = agency_decorations
    
    def find(self, agency_id: str, vehicle_id: str) -> Decoration | None:
        '''Returns the decorations with the given vehicle ID'''
        try:
            return self.decorations[agency_id][vehicle_id]
        except KeyError:
            return None
