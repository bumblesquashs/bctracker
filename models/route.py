
import re

from random import randint, seed
from math import sqrt
from colorsys import hls_to_rgb

import helpers.departure
import helpers.system

from models.daterange import DateRange
from models.match import Match
from models.schedule import Schedule

import utils

class Route:
    '''A list of trips that follow a regular pattern with a given number'''
    
    __slots__ = (
        'system',
        'id',
        'number',
        'key',
        'name',
        'colour',
        'text_colour'
    )
    
    @classmethod
    def from_db(cls, row, prefix='route'):
        system = helpers.system.default.find(row[f'{prefix}_system_id'])
        id = row[f'{prefix}_id']
        number = row[f'{prefix}_number']
        name = row[f'{prefix}_name']
        colour = row[f'{prefix}_colour'] or generate_colour(system, number)
        text_colour = row[f'{prefix}_text_colour'] or 'FFFFFF'
        return cls(system, id, number, name, colour, text_colour)
    
    @property
    def display_name(self):
        '''Formats the route name for web display'''
        return self.name.replace('/', '/<wbr />')
    
    @property
    def cache(self):
        '''Returns the cache for this route'''
        return self.system.get_route_cache(self)
    
    @property
    def trips(self):
        '''Returns the trips for this route'''
        return self.cache.trips
    
    @property
    def schedule(self):
        '''Returns the schedule for this route'''
        return self.cache.schedule
    
    @property
    def sheets(self):
        '''Returns the sheets for this route'''
        return self.cache.sheets
    
    @property
    def indicator_points(self):
        '''Returns the indicator points for this route'''
        return self.cache.indicator_points
    
    def __init__(self, system, id, number, name, colour, text_colour):
        self.system = system
        self.id = id
        self.number = number
        self.name = name
        self.colour = colour
        self.text_colour = text_colour
        
        self.key = utils.key(number)
    
    def __str__(self):
        return f'{self.number} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.key < other.key
    
    def __gt__(self, other):
        return self.key > other.key
    
    def get_json(self):
        '''Returns a representation of this route in JSON-compatible format'''
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'colour': self.colour,
            'text_colour': self.text_colour
        }
    
    def get_indicator_json(self):
        '''Returns a representation of the map indicator for this route in JSON-compatible format'''
        json = []
        for point in self.indicator_points:
            json.append({
                'system_id': self.system.id,
                'number': self.number,
                'name': self.name.replace("'", '&apos;'),
                'colour': self.colour,
                'text_colour': self.text_colour,
                'lat': point.lat,
                'lon': point.lon
            })
        return json
    
    def get_trips(self, service_group=None, date=None):
        '''Returns all trips from this route'''
        if service_group is None:
            if date is None:
                return sorted(self.trips)
            return sorted([t for t in self.trips if date in t.service])
        return sorted([t for t in self.trips if t.service in service_group])
    
    def get_headsigns(self, service_group=None, date=None):
        '''Returns all headsigns from this route'''
        return sorted({str(t) for t in self.get_trips(service_group, date)})
    
    def get_match(self, query):
        '''Returns a match for this route with the given query'''
        query = query.lower()
        number = self.number.lower()
        name = str(self).lower()
        value = 0
        if query in number:
            value += (len(query) / len(number)) * 100
            if number.startswith(query):
                value += len(query)
        elif query in name:
            value += (len(query) / len(name)) * 100
            if name.startswith(query):
                value += len(query)
        return Match(f'Route {self.number}', self.name, 'route', f'routes/{self.number}', value)
    
    def find_departures(self):
        '''Returns all departures for this route'''
        return helpers.departure.default.find_all(self.system, route=self)

def generate_colour(system, number):
    '''Generate a random colour based on system ID and route number'''
    seed(system.id)
    number_digits = ''.join([d for d in number if d.isdigit()])
    if len(number_digits) == 0:
        h = randint(1, 360) / 360.0
    else:
        h = (randint(1, 360) + (int(number_digits) * 137.508)) / 360.0
    seed(system.id + number)
    l = randint(30, 50) / 100.0
    s = randint(50, 100) / 100.0
    rgb = hls_to_rgb(h, l, s)
    r = int(rgb[0] * 255)
    g = int(rgb[1] * 255)
    b = int(rgb[2] * 255)
    return f'{r:02x}{g:02x}{b:02x}'

class RouteCache:
    '''A collection of calculated values for a single route'''
    
    __slots__ = (
        'trips',
        'schedule',
        'sheets',
        'indicator_points'
    )
    
    def __init__(self, system, trips):
        self.trips = trips
        services = {t.service for t in trips}
        self.sheets = system.copy_sheets(services)
        if self.sheets:
            date_range = DateRange.combine([s.schedule.date_range for s in self.sheets])
            self.schedule = Schedule.combine(services, date_range)
        else:
            self.schedule = None
        try:
            sorted_trips = sorted(trips, key=lambda t: t.departure_count, reverse=True)
            points = sorted_trips[0].find_points()
            first_point = points[0]
            last_point = points[-1]
            distance = sqrt(((first_point.lat - last_point.lat) ** 2) + ((first_point.lon - last_point.lon) ** 2))
            if distance <= 0.05:
                count = min((len(points) // 500) + 1, 3)
            else:
                count = min(int(distance * 8) + 1, 4)
            size = len(points) // count
            self.indicator_points = [points[(i * size) + (size // 2)] for i in range(count)]
        except IndexError:
            self.indicator_points = []
