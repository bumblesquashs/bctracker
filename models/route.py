
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.point import Point
    from models.sheet import Sheet
    from models.trip import Trip

from dataclasses import dataclass, field
from random import randint, seed
from math import sqrt
from colorsys import hls_to_rgb

from models.context import Context
from models.daterange import DateRange
from models.match import Match
from models.row import Row
from models.schedule import Schedule

import helpers
import repositories

@dataclass(slots=True)
class Route:
    '''A list of trips that follow a regular pattern with a given number'''
    
    context: Context
    id: str
    number: str
    name: str
    colour: str
    text_colour: str
    
    key: str = field(init=False)
    
    _trips: list[Trip] | None = field(default=None, init=False)
    _headsigns: list[str] | None = field(default=None, init=False)
    _schedule: Schedule | None = field(default=None, init=False)
    _sheets: list[Sheet] | None = field(default=None, init=False)
    _indicator_points: list[Point] | None = field(default=None, init=False)
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a route initialized from the given database row'''
        context = row.context()
        id = row['id']
        number = row['number'] or id
        name = row['name']
        colour = row['colour'] or generate_colour(context, number)
        text_colour = row['text_colour'] or 'FFFFFF'
        return cls(context, id, number, name, colour, text_colour)
    
    @property
    def url_id(self):
        '''The ID to use when making route URLs'''
        if self.context.prefer_route_id:
            return self.id
        return self.number
    
    @property
    def display_name(self):
        '''Formats the route name for web display'''
        return self.name.replace('/', '/<wbr />')
    
    @property
    def trips(self):
        '''Returns the trips for this route'''
        if self._trips is None:
            self._trips = repositories.trip.find_all(self.context, route=self)
        return self._trips
    
    @property
    def headsigns(self):
        if self._headsigns is None:
            headsigns = set()
            for trip in self.trips:
                headsigns.add(str(trip))
                for headsign in trip.custom_headsigns:
                    headsigns.add(headsign)
            self._headsigns = sorted(headsigns)
        return self._headsigns
    
    @property
    def schedule(self):
        '''Returns the schedule for this route'''
        if self.sheets:
            if self._schedule is None:
                services = {t.service for t in self.trips}
                date_range = DateRange.combine([s.schedule.date_range for s in self.sheets])
                self._schedule = Schedule.combine(services, date_range)
            return self._schedule
        return None
    
    @property
    def sheets(self):
        '''Returns the sheets for this route'''
        if self._sheets is None:
            services = {t.service for t in self.trips}
            self._sheets = self.context.system.copy_sheets(services)
        return self._sheets
    
    @property
    def indicator_points(self):
        '''Returns the indicator points for this route'''
        if self._indicator_points is None:
            try:
                sorted_trips = sorted(self.trips, key=lambda t: len(t.departures), reverse=True)
                points = sorted_trips[0].find_points()
                first_point = points[0]
                last_point = points[-1]
                distance = sqrt(((first_point.lat - last_point.lat) ** 2) + ((first_point.lon - last_point.lon) ** 2))
                if distance <= 0.05:
                    count = min((len(points) // 500) + 1, 3)
                else:
                    count = min(int(distance * 8) + 1, 4)
                size = len(points) // count
                self._indicator_points = [points[(i * size) + (size // 2)] for i in range(count)]
            except IndexError:
                self._indicator_points = []
        return self._indicator_points
    
    def __post_init__(self):
        self.key = helpers.key(self.number)
    
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
            'text_colour': self.text_colour,
            'url_id': self.url_id
        }
    
    def get_indicator_json(self):
        '''Returns a representation of the map indicator for this route in JSON-compatible format'''
        json = []
        for point in self.indicator_points:
            json.append({
                'system_id': self.context.system_id,
                'system_name': str(self.context.system),
                'agency_id': self.context.agency_id,
                'number': self.number,
                'name': self.name.replace("'", '&apos;'),
                'colour': self.colour,
                'text_colour': self.text_colour,
                'lat': point.lat,
                'lon': point.lon,
                'url_id': self.url_id,
                'headsigns': self.headsigns
            })
        return json
    
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
        return Match(f'Route {self.number}', self.name, 'route', f'routes/{self.url_id}', value)
    
    def is_variant(self, route):
        '''Checks if this route is a variant of another route'''
        if self == route:
            return False # Self is not a variant
        self_key = tuple([k for k in self.key if type(k) == int])
        route_key = tuple([k for k in route.key if type(k) == int])
        return self_key and route_key and self_key == route_key

def generate_colour(context: Context, number):
    '''Generate a random colour based on context and route number'''
    seed(context.system_id)
    number_digits = ''.join([d for d in number if d.isdigit()])
    if len(number_digits) == 0:
        h = randint(1, 360) / 360.0
    else:
        h = (randint(1, 360) + (int(number_digits) * 137.508)) / 360.0
    seed(context.system_id + number)
    l = randint(30, 50) / 100.0
    s = randint(50, 100) / 100.0
    rgb = hls_to_rgb(h, l, s)
    r = int(rgb[0] * 255)
    g = int(rgb[1] * 255)
    b = int(rgb[2] * 255)
    return f'{r:02x}{g:02x}{b:02x}'
