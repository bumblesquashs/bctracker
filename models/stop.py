
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.departure import Departure
    from models.route import Route
    from models.sheet import Sheet

from dataclasses import dataclass, field
from math import sqrt

from models.context import Context
from models.daterange import DateRange
from models.row import Row
from models.schedule import Schedule

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
    
    _departures: list[Departure] | None = field(default=None, init=False)
    _routes: list[Route] | None = field(default=None, init=False)
    _schedule: Schedule | None = field(default=None, init=False)
    _sheets: list[Sheet] | None = field(default=None, init=False)
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a stop initialized from the given database row'''
        context = row.context()
        id = row['id']
        number = row['number'] or id
        name = row['name']
        lat = row['lat']
        lon = row['lon']
        return cls(context, id, number, name, lat, lon)
    
    @property
    def url_id(self):
        '''The ID to use when making stop URLs'''
        if self.context.prefer_stop_id:
            return self.id
        return self.number
    
    @property
    def departures(self):
        '''Returns the departures for this stop'''
        if self._departures is None:
            self._departures = repositories.departure.find_all(self.context, stop=self)
        return self._departures
    
    @property
    def routes(self):
        '''Returns the routes for this stop'''
        if self._routes is None:
            self._routes = repositories.route.find_all(self.context, stop=self)
        return self._routes
    
    @property
    def schedule(self):
        '''Returns the schedule for this stop'''
        if self.sheets:
            if self._schedule is None:
                services = {d.trip.service for d in self.departures if d.trip}
                date_range = DateRange.combine([s.schedule.date_range for s in self.sheets])
                self._schedule = Schedule.combine(services, date_range)
            return self._schedule
        return None
    
    @property
    def sheets(self):
        '''Returns the sheets for this stop'''
        if self._sheets is None:
            services = {d.trip.service for d in self.departures if d.trip}
            self._sheets = self.context.system.copy_sheets(services)
        return self._sheets
    
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
    
    def is_near(self, lat, lon, accuracy=0.001):
        '''Checks if this stop is near the given latitude and longitude'''
        return sqrt(((self.lat - lat) ** 2) + ((self.lon - lon) ** 2)) <= accuracy
    
    def find_departures(self, service_group=None, date=None):
        '''Returns all departures from this stop'''
        if service_group:
            return sorted([d for d in self.departures if d.trip and d.trip.service in service_group])
        if date:
            return sorted([d for d in self.departures if d.trip and date in d.trip.service])
        return sorted(self.departures)
