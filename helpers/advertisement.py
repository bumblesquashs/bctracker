
import csv
import random

from models.advertisement import Advertisement

advertisements = []

def load():
    '''Loads advertisement data from the static CSV file'''
    global advertisements
    with open(f'./data/static/advertisements.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        advertisements = [Advertisement.from_csv(dict(zip(columns, row))) for row in reader]

def find_random():
    return random.choice(advertisements)
