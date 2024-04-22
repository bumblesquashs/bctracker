
from math import sqrt

from di import di

from models.daterange import DateRange
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
        'lon'
    )
    
    @classmethod
    def from_db(cls, row, prefix='stop'):
        from helpers.system import SystemService
        system = di[SystemService].find(row[f'{prefix}_system_id'])
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
    def cache(self):
        '''Returns the cache for this stop'''
        return self.system.get_stop_cache(self)
    
    @property
    def schedule(self):
        '''Returns the schedule for this stop'''
        return self.cache.schedule
    
    @property
    def sheets(self):
        '''Returns the sheets for this stop'''
        return self.cache.sheets
    
    @property
    def routes(self):
        '''Returns the routes for this stop'''
        return self.cache.routes
    
    def __init__(self, system, id, number, name, lat, lon):
        self.system = system
        self.id = id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
    
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
        from helpers.departure import DepartureService
        departures = di[DepartureService].find_all(self.system, stop=self)
        if service_group is None:
            if date is None:
                return sorted(departures)
            return sorted([d for d in departures if d.trip is not None and date in d.trip.service])
        return sorted([d for d in departures if d.trip is not None and d.trip.service in service_group])
    
    def find_adjacent_departures(self):
        '''Returns all departures on trips that serve this stop'''
        from helpers.departure import DepartureService
        return di[DepartureService].find_adjacent(self.system, self)

class StopCache:
    '''A collection of calculated values for a single stop'''
    
    __slots__ = (
        'schedule',
        'sheets',
        'routes'
    )
    
    def __init__(self, system, departures):
        services = {d.trip.service for d in departures if d.trip is not None}
        self.sheets = system.copy_sheets(services)
        if self.sheets:
            date_range = DateRange.combine([s.schedule.date_range for s in self.sheets])
            self.schedule = Schedule.combine(services, date_range)
        else:
            self.schedule = None
        self.routes = sorted({d.trip.route for d in departures if d.trip is not None and d.trip.route is not None})
