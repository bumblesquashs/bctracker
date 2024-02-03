
import csv

from models.agency import Agency

agencies = {}

def load():
    '''Loads agency data from the static CSV file'''
    with open(f'./static/agencies.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            agency = Agency.from_csv(dict(zip(columns, row)))
            agencies[agency.id] = agency

def find(agency_id):
    '''Returns the agency with the given ID'''
    if agency_id is not None and agency_id in agencies:
        return agencies[agency_id]
    return None

def find_all():
    '''Returns all agencies'''
    return agencies.values()

def delete_all():
    '''Deletes all agencies'''
    global agencies
    agencies = {}
