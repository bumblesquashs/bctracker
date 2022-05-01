
from enum import Enum

import csv

class BusModelType(Enum):
    artic = "Articulated"
    conventional = "Conventional"
    decker = "Double Decker"
    shuttle = "Shuttle"

class BusModel:
    __slots__ = ('id', 'manufacturer', 'name', 'length', 'fuel', 'type')
    
    def __init__(self, row):
        self.id = row['model_id']
        self.manufacturer = row['manufacturer']
        self.name = row['name']
        self.length = float(row['length'])
        self.fuel = row['fuel']
        self.type = BusModelType[row['type']]
    
    def __str__(self):
        return f'{self.manufacturer} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)

models = {}

def load_models():
    rows = []
    with open(f'./static_data/models.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    for row in rows:
        model = BusModel(row)
        models[model.id] = model

def get_model(model_id):
    return models.get(model_id)
