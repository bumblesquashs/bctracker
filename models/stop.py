
from math import sqrt

import helpers.departure
import helpers.route
import helpers.sheet
import helpers.system

from models.match import Match
from models.schedule import Schedule

class Stop:
    '''A location where a vehicle stops along a trip'''
    
    __slots__ = (
        'system',
        'id',
        'number',
        'name',
        'lat',
        'lon',
        'is_setup',
        '_schedule',
        '_sheets',
        '_routes'
    )
    
    @classmethod
    def from_db(cls, row, prefix='stop'):
        system = helpers.system.find(row[f'{prefix}_system_id'])
        id = row[f'{prefix}_id']
        number = row[f'{prefix}_number']
        name = row[f'{prefix}_name']
        lat = row[f'{prefix}_lat']
        lon = row[f'{prefix}_lon']
        return cls(system, id, number, name, lat, lon)
    
    @property
    def nearby_stops(self):
        '''Returns all stops with coordinates close to this stop'''
        stops = self.system.get_stops()
        return sorted({s for s in stops if s.is_near(self.lat, self.lon) and self != s})
    
    @property
    def schedule(self):
        self.setup()
        return self._schedule
    
    @property
    def sheets(self):
        self.setup()
        return self._sheets
    
    @property
    def routes(self):
        self.setup()
        return self._routes
    
    def __init__(self, system, id, number, name, lat, lon):
        self.system = system
        self.id = id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
        
        self.is_setup = False
        self._schedule = None
        self._sheets = []
        self._routes = []
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.name == other.name:
            return self.number < other.number
        return self.name < other.name
    
    def setup(self, departures=None):
        if self.is_setup:
            return
        self.is_setup = True
        if departures is None:
            departures = helpers.departure.find_all(self.system, stop=self)
        services = {d.trip.service for d in departures if d.trip is not None}
        self._schedule = Schedule.combine(services)
        self._sheets = self.system.copy_sheets(services)
        self._routes = sorted({d.trip.route for d in departures if d.trip is not None and d.trip.route is not None})
    
    def get_json(self):
        '''Returns a representation of this stop in JSON-compatible format'''
        return {
            'system_id': self.system.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'lat': self.lat,
            'lon': self.lon,
            'routes': [r.get_json() for r in self.routes]
        }
    
    def get_match(self, query):
        '''Returns a match for this stop with the given query'''
        query = query.lower()
        number = self.number.lower()
        name = self.name.lower()
        value = 0
        if query in number:
            value += (len(query) / len(number)) * 100
            if number.startswith(query):
                value += len(query)
        elif query in name:
            value += (len(query) / len(name)) * 100
            if name.startswith(query):
                value += len(query)
            if value > 20:
                value -= 20
            else:
                value = 1
        return Match(f'Stop {self.number}', self.name, 'stop', f'stops/{self.number}', value)
    
    def is_near(self, lat, lon, accuracy=0.001):
        '''Checks if this stop is near the given latitude and longitude'''
        return sqrt(((self.lat - lat) ** 2) + ((self.lon - lon) ** 2)) <= accuracy
    
    def find_departures(self, service_group=None, date=None):
        '''Returns all departures from this stop'''
        departures = helpers.departure.find_all(self.system, stop=self)
        if service_group is None:
            if date is None:
                return sorted(departures)
            return sorted([d for d in departures if d.trip is not None and date in d.trip.service])
        return sorted([d for d in departures if d.trip is not None and d.trip.service in service_group])
    
    def find_adjacent_departures(self):
        '''Returns all departures on trips that serve this stop'''
        return helpers.departure.find_adjacent(self.system, self)
