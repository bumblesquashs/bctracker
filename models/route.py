
import re

from os.path import commonprefix
from random import randint, seed
from math import sqrt
from colorsys import hls_to_rgb

import helpers.bcf_scraper

from models.match import Match
from models.schedule import Schedule

class Route:
    '''A list of trips that follow a regular pattern with a given number'''
    
    __slots__ = ('system', 'id', 'number', 'key', 'name', 'colour', 'text_colour', 'trips', 'schedule', 'sheets', 'indicator_points')
    
    @classmethod
    def from_csv(cls, row, system, trips):
        '''Returns a route initialized from the given CSV row'''
        id = row['route_id']
        route_trips = trips.get(id, [])
        number = row['route_short_name']
        if system.is_bcf and 'route_long_name' in row:
            number = str(helpers.bcf_scraper.get_route_number(row['route_long_name']))
        if 'route_long_name' in row and row['route_long_name'] != '':
            name = row['route_long_name']
        else:
            headsigns = sorted(t.headsign for t in route_trips)
            for i in range(len(headsigns)):
                headsign = headsigns[i]
                if not system.prefix_headsign:
                    headsign = headsign.lstrip(number).strip(' ')
                if headsign.startswith('A '):
                    headsign.lstrip('A ')
                if headsign.startswith('B '):
                    headsign.lstrip('B ')
                if ' - ' in headsign:
                    headsign = headsign.split(' - ')[0]
                elif '- ' in headsign:
                    headsign = headsign.split('- ')[0]
                elif ' to ' in headsign:
                    headsign = headsign.split(' to ')[0]
                elif ' To ' in headsign:
                    headsign = headsign.split(' To ')[0]
                elif ' via ' in headsign:
                    headsign = headsign.split(' via ')[0]
                elif ' Via ' in headsign:
                    headsign = headsign.split(' Via ')[0]
                headsigns[i] = headsign.strip(' ').strip(',')
            prefix = commonprefix(headsigns).strip(' ')
            if len(prefix) < 3:
                if len(headsigns) > 2:
                    headsigns = [h for h in headsigns if not h.startswith('To ')]
                name = ' / '.join(sorted(set(headsigns)))
            else:
                name = prefix
        if 'route_color' in row and row['route_color'] != '' and (not system.recolour_black or row['route_color'] != '000000'):
            colour = row['route_color']
        else:
            # Generate a random colour based on system ID and route number
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
            colour = f'{r:02x}{g:02x}{b:02x}'
        if 'route_text_color' in row and row['route_text_color'] != '':
            text_colour = row['route_text_color']
        else:
            text_colour = 'FFFFFF'
        return cls(system, id, number, name, colour, text_colour, route_trips)
    
    def __init__(self, system, id, number, name, colour, text_colour, trips):
        self.system = system
        self.id = id
        self.number = number
        self.name = name
        self.colour = colour
        self.text_colour = text_colour
        self.trips = trips
        
        if len(trips) == 0:
            self.indicator_points = []
        else:
            sorted_trips = sorted(trips, key=lambda t: len(t.departures), reverse=True)
            points = sorted_trips[0].load_points()
            first_point = points[0]
            last_point = points[-1]
            distance = sqrt(((first_point.lat - last_point.lat) ** 2) + ((first_point.lon - last_point.lon) ** 2))
            if distance <= 0.05:
                count = min((len(points) // 500) + 1, 3)
            else:
                count = min(int(distance * 8) + 1, 4)
            size = len(points) // count
            self.indicator_points = [points[(i * size) + (size // 2)] for i in range(count)]
        
        self.key = tuple([int(s) if s.isnumeric() else s for s in re.split('([0-9]+)', number)])
        
        services = {t.service for t in self.trips}
        self.schedule = Schedule.combine([s.schedule for s in services])
        self.sheets = system.copy_sheets(services)
    
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
    
    @property
    def display_name(self):
        '''Formats the route name for web display'''
        return self.name.replace('/', '/<wbr />')
    
    @property
    def json(self):
        '''Returns a representation of this route in JSON-compatible format'''
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'colour': self.colour,
            'text_colour': self.text_colour
        }
    
    @property
    def indicator_json(self):
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
            return sorted([t for t in self.trips if date in t.service.schedule])
        return sorted([t for t in self.trips if t.service in service_group.services])
    
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
        return Match('route', self.number, self.name, f'routes/{self.number}', value)
