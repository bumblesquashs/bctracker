
import json

from models.region import Region

regions = {}

def load():
    '''Loads region data from the static JSON file'''
    global regions
    regions = {}
    with open(f'./static/regions.json', 'r') as file:
        for (id, values) in json.load(file).items():
            regions[id] = Region(id, **values)

def find(region_id):
    '''Returns the region with the given ID'''
    try:
        return regions[region_id]
    except KeyError:
        return None

def find_all():
    '''Returns all regions'''
    return regions.values()
