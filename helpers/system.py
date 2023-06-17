
import csv

from models.system import System

systems = {}

def load():
    '''Loads system data from the static CSV file'''
    with open(f'./data/static/systems.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            system = System.from_csv(dict(zip(columns, row)))
            systems[system.id] = system

def find(system_id):
    '''Returns the system with the given ID'''
    if system_id is not None and system_id in systems:
        return systems[system_id]
    return None

def find_all():
    '''Returns all systems'''
    return systems.values()

def delete_all():
    '''Deletes all systems'''
    global systems
    systems = {}
