
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.agency import Agency
    from models.system import System

from dataclasses import dataclass, field
from enum import Enum
from random import randint, seed
from math import sqrt
from colorsys import hls_to_rgb

from models.context import Context
from models.daterange import DateRange
from models.match import Match
from models.point import Point
from models.row import Row
from models.schedule import Schedule
from models.sheet import Sheet
from models.trip import Trip

import helpers

class RouteType(Enum):
    '''Options for route types'''
    
    UNKNOWN = ''
    LIGHT_RAIL = '0'
    METRO = '1'
    RAIL = '2'
    BUS = '3'
    FERRY = '4'
    CABLE_CAR = '5'
    AERIAL_LIFT = '6'
    FUNICULAR = '7'
    TROLLEY_BUS = '11'
    MONORAIL = '12'
    
    @classmethod
    def from_db(cls, value):
        try:
            return cls(value)
        except:
            return cls.UNKNOWN
    
    def __str__(self):
        match self:
            case RouteType.UNKNOWN:
                return 'Unknown'
            case RouteType.LIGHT_RAIL:
                return 'Light Rail'
            case RouteType.METRO:
                return 'Metro'
            case RouteType.RAIL:
                return 'Rail'
            case RouteType.BUS:
                return 'Bus'
            case RouteType.FERRY:
                return 'Ferry'
            case RouteType.CABLE_CAR:
                return 'Cable Car'
            case RouteType.AERIAL_LIFT:
                return 'Gondola'
            case RouteType.FUNICULAR:
                return 'Funicular'
            case RouteType.TROLLEY_BUS:
                return 'Trolley Bus'
            case RouteType.MONORAIL:
                return 'Monorail'

@dataclass(slots=True)
class Route:
    '''A list of trips that follow a regular pattern with a given number'''
    
    agency: Agency
    system: System
    id: str
    number: str
    name: str
    colour: str
    text_colour: str
    type: RouteType
    sort_order: int | None
    
    key: str = field(init=False)
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a route initialized from the given database row'''
        context = row.context()
        id = row['route_id']
        number = row['number'] or id
        name = row['name']
        colour = row['colour'] or generate_colour(context, number)
        text_colour = row['text_colour'] or 'FFFFFF'
        type = RouteType.from_db(row['type'])
        sort_order = row['sort_order']
        return cls(context.agency, context.system, id, number, name, colour, text_colour, type, sort_order)
    
    @property
    def context(self):
        '''The context for this route'''
        return self.system.context
    
    @property
    def url_id(self):
        '''The ID to use when making route URLs'''
        if self.context.prefer_route_id:
            return self.id.replace('/', '-and-')
        return self.number.replace('/', '-and-')
    
    @property
    def display_name(self):
        '''Formats the route name for web display'''
        return self.name.replace('/', '/<wbr />')
    
    @property
    def cache(self):
        '''Returns the cache for this route'''
        return self.system.get_route_cache(self.id)
    
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
    
    def __post_init__(self):
        self.key = helpers.key(self.number)
    
    def __str__(self):
        return f'{self.number} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.sort_order is not None and other.sort_order is not None:
            return self.sort_order < other.sort_order
        return self.key < other.key
    
    def __gt__(self, other):
        if self.sort_order is not None and other.sort_order is not None:
            return self.sort_order > other.sort_order
        return self.key > other.key
    
    def get_json(self):
        '''Returns a representation of this route in JSON-compatible format'''
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'colour': self.colour,
            'text_colour': self.text_colour,
            'type': str(self.type),
            'url_id': self.url_id
        }
    
    def get_indicator_json(self):
        '''Returns a representation of the map indicator for this route in JSON-compatible format'''
        json = []
        for point in self.indicator_points:
            json.append({
                'system_id': self.system.id,
                'system_name': str(self.system),
                'agency_id': self.context.agency_id,
                'number': self.number,
                'name': self.name.replace("'", '&apos;'),
                'colour': self.colour,
                'text_colour': self.text_colour,
                'type': str(self.type),
                'lat': point.lat,
                'lon': point.lon,
                'url_id': self.url_id,
                'headsigns': self.get_headsigns()
            })
        return json
    
    def get_trips(self, service_group=None, date=None):
        '''Returns all trips from this route'''
        if service_group:
            return sorted([t for t in self.trips if t.service in service_group])
        if date:
            return sorted([t for t in self.trips if date in t.service])
        return sorted(self.trips)
    
    def get_headsigns(self, service_group=None, date=None):
        '''Returns all headsigns from this route'''
        headsigns = set()
        for trip in self.get_trips(service_group, date):
            headsigns.add(str(trip))
            for headsign in trip.custom_headsigns:
                headsigns.add(headsign)
        return sorted(headsigns)
    
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

@dataclass(slots=True)
class RouteCache:
    '''A collection of calculated values for a single route'''
    
    trips: list[Trip]
    schedule: Schedule | None
    sheets: list[Sheet]
    indicator_points: list[Point]
    
    @classmethod
    def build(cls, system, trips):
        services = {t.service for t in trips}
        sheets = system.copy_sheets(services)
        if sheets:
            date_range = DateRange.combine([s.schedule.date_range for s in sheets])
            schedule = Schedule.combine(services, date_range)
        else:
            schedule = None
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
            indicator_points = [points[(i * size) + (size // 2)] for i in range(count)]
        except IndexError:
            indicator_points = []
        return cls(trips, schedule, sheets, indicator_points)
