
from dataclasses import dataclass, field
import json

from models.model import Model, ModelType

@dataclass(slots=True)
class ModelRepository:
    
    models: dict[str, Model] = field(default_factory=dict)
    
    def load(self):
        '''Loads model data from the static JSON file'''
        self.models = {}
        with open(f'./config/models.json', 'r') as file:
            values = json.load(file)
        for (id, model_values) in values.items():
            type_id = model_values['type']
            model_values['type'] = ModelType[type_id.upper()]
            self.models[id] = Model(id, **model_values)
    
    def find(self, model_id: str) -> Model | None:
        '''Returns the model with the given ID'''
        return self.models.get(model_id)
