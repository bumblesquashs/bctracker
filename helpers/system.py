
import csv

from models.system import System

systems = {}

def load():
    with open(f'./data/static/systems.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            system = System.from_csv(dict(zip(columns, row)))
            systems[system.id] = system

def find(system_id):
    if system_id is not None and system_id in systems:
        return systems[system_id]
    return None

def find_all():
    return systems.values()
