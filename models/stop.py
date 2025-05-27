
from math import sqrt

from di import di

from models.context import Context
from models.daterange import DateRange
from models.match import Match
from models.schedule import Schedule

from repositories import DepartureRepository

import helpers

class Stop:
    '''A location where a vehicle stops along a trip'''
    
    __slots__ = (
        'departure_repository',
        'context',
        'id',
        'number',
        'key',
        'name',
        'lat',
        'lon'
    )
    
    @classmethod
    def from_db(cls, row, prefix='stop'):
        '''Returns a stop initialized from the given database row'''
        context = Context.find(system_id=row[f'{prefix}_system_id'])
        id = row[f'{prefix}_id']
        number = row[f'{prefix}_number']
        if not number:
            number = id
        name = row[f'{prefix}_name']
        lat = row[f'{prefix}_lat']
        lon = row[f'{prefix}_lon']
        return cls(context, id, number, name, lat, lon)
    
    @property
    def url_id(self):
        '''The ID to use when making stop URLs'''
        if self.context.prefer_stop_id:
            return self.id
        return self.number
    
    @property
    def nearby_stops(self):
        '''Returns all stops with coordinates close to this stop'''
        stops = self.context.system.get_stops()
        return sorted({s for s in stops if s.is_near(self.lat, self.lon) and self != s})
    
    @property
    def cache(self):
        '''Returns the cache for this stop'''
        return self.context.system.get_stop_cache(self)
    
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
    
    def __init__(self, context: Context, id, number, name, lat, lon, **kwargs):
        self.context = context
        self.id = id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
        
        self.key = helpers.key(number)
        
        self.departure_repository = kwargs.get('departure_repository') or di[DepartureRepository]
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.name == other.name:
            return self.key < other.key
        return self.name < other.name
    
    def get_json(self):
        '''Returns a representation of this stop in JSON-compatible format'''
        number = self.number if self.context.show_stop_number else None
        return {
            'system_id': self.context.system_id,
            'system_name': str(self.context.system),
            'agency_id': self.context.agency_id,
            'number': number,
            'name': self.name.replace("'", '&apos;'),
            'lat': self.lat,
            'lon': self.lon,
            'routes': [r.get_json() for r in self.routes],
            'url_id': self.url_id
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
        return Match(f'Stop {self.number}', self.name, 'stop', f'stops/{self.url_id}', value)
    
    def is_near(self, lat, lon, accuracy=0.001):
        '''Checks if this stop is near the given latitude and longitude'''
        return sqrt(((self.lat - lat) ** 2) + ((self.lon - lon) ** 2)) <= accuracy
    
    def find_departures(self, service_group=None, date=None):
        '''Returns all departures from this stop'''
        departures = self.departure_repository.find_all(self.context, stop=self)
        if service_group:
            return sorted([d for d in departures if d.trip and d.trip.service in service_group])
        if date:
            return sorted([d for d in departures if d.trip and date in d.trip.service])
        return sorted(departures)
    
    def find_adjacent_departures(self):
        '''Returns all departures on trips that serve this stop'''
        return self.departure_repository.find_adjacent(self.context, self)

class StopCache:
    '''A collection of calculated values for a single stop'''
    
    __slots__ = (
        'schedule',
        'sheets',
        'routes'
    )
    
    def __init__(self, system, departures):
        services = {d.trip.service for d in departures if d.trip}
        self.sheets = system.copy_sheets(services)
        if self.sheets:
            date_range = DateRange.combine([s.schedule.date_range for s in self.sheets])
            self.schedule = Schedule.combine(services, date_range)
        else:
            self.schedule = None
        self.routes = sorted({d.trip.route for d in departures if d.trip and d.trip.route})
