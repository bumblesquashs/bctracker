
import csv
import random

from models.advertisement import Advertisement
from models.time import Time

advertisements = []

def load():
    '''Loads advertisement data from the static CSV file'''
    global advertisements
    with open(f'./data/static/advertisements.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        advertisements = [Advertisement.from_csv(dict(zip(columns, row))) for row in reader]

def find_random():
    now = Time.now()
    if now.hour < 12:
        return random.choice([a for a in advertisements if a.id != 'april-fools'])
    return random.choice(advertisements)
