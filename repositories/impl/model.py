
from dataclasses import dataclass, field
import json

from models.model import Model, ModelType

@dataclass(slots=True)
class ModelRepository:
    
    models: dict[str, Model] = field(default_factory=dict)
    
    def load(self):
        '''Loads model data from the static JSON file'''
        self.models = {}
        with open(f'./static/models.json', 'r') as file:
            for (type_id, type_values) in json.load(file).items():
                type = ModelType[type_id]
                for (id, values) in type_values.items():
                    self.models[id] = Model(id, type, **values)
    
    def find(self, model_id) -> Model | None:
        '''Returns the model with the given ID'''
        return self.models.get(model_id)
