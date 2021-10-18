
from enum import Enum

import csv

class BusModelType(Enum):
    artic = "Articulated"
    conventional = "Conventional"
    decker = "Double Decker"
    shuttle = "Shuttle"

class BusModel:
    def __init__(self, model_id, manufacturer, name, length, fuel, type):
        self.id = model_id
        self.manufacturer = manufacturer
        self.name = name
        self.length = length
        self.fuel = fuel
        self.type = BusModelType[type]
    
    def __str__(self):
        return f'{self.manufacturer} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.manufacturer == other.manufacturer:
            return self.name < other.name
        return self.manufacturer < other.manufacturer

models = {}

def load_models():
    rows = []
    with open(f'./static_data/models.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    for row in rows:
        model_id = row['model_id']
        manufacturer = row['manufacturer']
        name = row['name']
        length = float(row['length'])
        fuel = row['fuel']
        type = row['type']

        models[model_id] = BusModel(model_id, manufacturer, name, length, fuel, type)

def get_model(model_id):
    return models.get(model_id)
