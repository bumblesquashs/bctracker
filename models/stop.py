
from math import sqrt

from models.match import Match
from models.service import create_service_group
from models.sheet import create_sheets

class Stop:
    '''A location where a vehicle stops along a trip'''
    
    __slots__ = ('system', 'id', 'number', 'name', 'lat', 'lon', 'departures', '_services', '_service_group', '_sheets')
    
    def __init__(self, system, row):
        self.system = system
        self.id = row['stop_id']
        self.number = row['stop_code']
        self.name = row['stop_name']
        self.lat = float(row['stop_lat'])
        self.lon = float(row['stop_lon'])
        
        self.departures = []
        self._services = None
        self._service_group = None
        self._sheets = None
    
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
    def services(self):
        if self._services is None:
            self._services = sorted({d.trip.service for d in self.departures})
        return self._services
    
    @property
    def service_group(self):
        if self._service_group is None:
            self._service_group = create_service_group(self.services)
        return self._service_group
    
    @property
    def sheets(self):
        if self._sheets is None:
            self._sheets = create_sheets(self.services)
        return self._sheets
    
    @property
    def is_current(self):
        for service in self.services:
            if self.system.get_sheet(service).is_current:
                return True
        return False
    
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
    
    def add_departure(self, departure):
        self.departures.append(departure)
        self._services = None
        self._service_group = None
        self._sheets = None
    
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
