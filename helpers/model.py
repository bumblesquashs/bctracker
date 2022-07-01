
import csv

from models.model import Model

models = {}

def load():
    with open(f'./data/static/models.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            model = Model.from_csv(dict(zip(columns, row)))
            models[model.id] = model

def find(model_id):
    if model_id in models:
        return models[model_id]
    return None
