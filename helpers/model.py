
import json

from models.model import Model, ModelType

models = {}

def load():
    '''Loads model data from the static JSON file'''
    global models
    models = {}
    with open(f'./static/models.json', 'r') as file:
        for (type_id, type_values) in json.load(file).items():
            type = ModelType[type_id]
            for (id, values) in type_values.items():
                models[id] = Model(id, type, **values)

def find(model_id):
    '''Returns the model with the given ID'''
    if model_id in models:
        return models[model_id]
    return None
