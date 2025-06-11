
from dataclasses import dataclass, field
from math import sqrt

from models.context import Context
from models.daterange import DateRange
from models.match import Match
from models.route import Route
from models.schedule import Schedule
from models.sheet import Sheet

import helpers
import repositories

@dataclass(slots=True)
class Stop:
    '''A location where a vehicle stops along a trip'''
    
    context: Context
    id: str
    number: str
    name: str
    lat: float
    lon: float
    
    key: str = field(init=False)
    
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
    
    def __post_init__(self):
        self.key = helpers.key(self.number)
    
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
        departures = repositories.departure.find_all(self.context, stop=self)
        if service_group:
            return sorted([d for d in departures if d.trip and d.trip.service in service_group])
        if date:
            return sorted([d for d in departures if d.trip and date in d.trip.service])
        return sorted(departures)
    
    def find_adjacent_departures(self):
        '''Returns all departures on trips that serve this stop'''
        return repositories.departure.find_adjacent(self.context, self)

@dataclass(slots=True)
class StopCache:
    '''A collection of calculated values for a single stop'''
    
    schedule: Schedule
    sheets: list[Sheet]
    routes: list[Route]
    
    @classmethod
    def build(cls, system, departures):
        services = {d.trip.service for d in departures if d.trip}
        sheets = system.copy_sheets(services)
        if sheets:
            date_range = DateRange.combine([s.schedule.date_range for s in sheets])
            schedule = Schedule.combine(services, date_range)
        else:
            schedule = None
        routes = sorted({d.trip.route for d in departures if d.trip and d.trip.route})
        return cls(schedule, sheets, routes)
