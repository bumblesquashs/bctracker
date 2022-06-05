
from math import sqrt

import helpers.sheet

from models.match import Match
from models.service import ServiceGroup

class Stop:
    '''A location where a vehicle stops along a trip'''
    
    __slots__ = ('system', 'id', 'number', 'name', 'lat', 'lon', 'departures', 'service_group', 'sheets')
    
    @classmethod
    def from_csv(cls, row, system, departures):
        id = row['stop_id']
        number = row['stop_code']
        name = row['stop_name']
        lat = float(row['stop_lat'])
        lon = float(row['stop_lon'])
        return cls(system, id, number, name, lat, lon, departures.get(id, []))
    
    def __init__(self, system, id, number, name, lat, lon, departures):
        self.system = system
        self.id = id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
        self.departures = sorted(departures)
        
        services = {d.trip.service for d in departures if d.trip is not None}
        self.service_group = ServiceGroup.combine(services)
        self.sheets = helpers.sheet.combine(services)
    
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
    
    @property
    def nearby_stops(self):
        stops = self.system.get_stops()
        return sorted({s for s in stops if sqrt(((self.lat - s.lat) ** 2) + ((self.lon - s.lon) ** 2)) <= 0.001 and self != s})
    
    @property
    def json(self):
        return {
            'system_id': self.system.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'lat': self.lat,
            'lon': self.lon,
            'routes': [r.json for r in self.get_routes()]
        }
    
    def get_departures(self, service_group=None):
        if service_group is None:
            return self.departures
        return [d for d in self.departures if d.trip.service in service_group.services]
    
    def get_routes(self, service_group=None):
        return sorted({d.trip.route for d in self.get_departures(service_group)})
    
    def get_routes_string(self, service_group=None):
        return ', '.join([r.number for r in self.get_routes(service_group)])
    
    def get_match(self, query):
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
        return Match('stop', self.number, self.name, f'stops/{self.number}', value)
