
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass, field
from enum import Enum
from math import sqrt

from models.daterange import DateRange
from models.match import Match
from models.route import Route
from models.row import Row
from models.schedule import Schedule
from models.sheet import Sheet

import helpers
import repositories

class StopType(Enum):
    '''Options for stop types'''
    
    STOP = '0'
    STATION = '1'
    ENTRANCE_EXIT = '2'
    NODE = '3'
    BOARDING_AREA = '4'
    
    @classmethod
    def from_db(cls, value):
        try:
            return cls(value)
        except:
            return cls.STOP
    
    def __str__(self):
        match self:
            case StopType.STOP:
                return 'Stop'
            case StopType.STATION:
                return 'Station'
            case StopType.ENTRANCE_EXIT:
                return 'Entrance/Exit'
            case StopType.NODE:
                return 'Node'
            case StopType.BOARDING_AREA:
                return 'Boarding Area'

@dataclass(slots=True)
class Stop:
    '''A location where a vehicle stops along a trip'''
    
    system: System
    id: str
    number: str
    name: str
    lat: float
    lon: float
    parent_id: str | None
    type: StopType
    
    key: str = field(init=False)
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a stop initialized from the given database row'''
        context = row.context()
        id = row['id']
        number = row['number'] or id
        name = row['name']
        lat = row['lat']
        lon = row['lon']
        parent_id = row['parent_id']
        type = StopType.from_db(row['type'])
        return cls(context.system, id, number, name, lat, lon, parent_id, type)
    
    @property
    def context(self):
        '''The context for this stop'''
        return self.system.context
    
    @property
    def url_id(self):
        '''The ID to use when making stop URLs'''
        if self.context.prefer_stop_id:
            return self.id
        return self.number
    
    @property
    def cache(self):
        '''Returns the cache for this stop'''
        return self.system.get_stop_cache(self.id)
    
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
            'system_id': self.system.id,
            'system_name': str(self.system),
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
        departures = repositories.departure.find_all(self.context, stop_id=self.id)
        if service_group:
            return sorted([d for d in departures if d.trip and d.trip.service in service_group])
        if date:
            return sorted([d for d in departures if d.trip and date in d.trip.service])
        return sorted(departures)
    
    def find_adjacent_departures(self):
        '''Returns all departures on trips that serve this stop'''
        return repositories.departure.find_adjacent(self.context, self.id)

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
