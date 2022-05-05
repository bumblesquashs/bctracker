
import csv

from models.model import Model

models = {}

def load():
    rows = []
    with open(f'./data/static/models.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    for row in rows:
        model = Model.from_csv(row)
        models[model.id] = model

def find(model_id):
    if model_id in models:
        return models[model_id]
    return None

