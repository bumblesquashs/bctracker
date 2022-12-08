
import csv

from models.region import Region

regions = {}

def load():
    '''Loads region data from the static CSV file'''
    with open(f'./data/static/regions.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            region = Region.from_csv(dict(zip(columns, row)))
            regions[region.id] = region

def find(region_id):
    '''Returns the region with the given ID'''
    if region_id is not None and region_id in regions:
        return regions[region_id]
    return None

def find_all():
    '''Returns all regions'''
    return regions.values()
