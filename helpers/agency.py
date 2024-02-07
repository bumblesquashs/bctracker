
import json

from models.agency import Agency

agencies = {}

def load():
    '''Loads agency data from the static JSON file'''
    global agencies
    agencies = {}
    with open(f'./static/agencies.json', 'r') as file:
        for (id, values) in json.load(file).items():
            agencies[id] = Agency(id, **values)

def find(agency_id):
    '''Returns the agency with the given ID'''
    if agency_id is not None and agency_id in agencies:
        return agencies[agency_id]
    return None

def find_all():
    '''Returns all agencies'''
    return agencies.values()
