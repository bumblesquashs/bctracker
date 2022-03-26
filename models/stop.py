
from math import sqrt

from models.search_result import SearchResult
from models.service import create_service_group
from models.sheet import create_sheets

class Stop:
    __slots__ = ('system', 'id', 'number', 'name', 'lat', 'lon', 'departures', '_services', '_service_group', '_sheets')
    
    def __init__(self, system, row):
        self.system = system
        self.id = row['stop_id']
        if 'stop_code' in row:
            self.number = row['stop_code']
        else:
            self.number = self.id
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
    def nearby_stops(self):
        stops = self.system.get_stops()
        return sorted({s for s in stops if sqrt(((self.lat - s.lat) ** 2) + ((self.lon - s.lon) ** 2)) <= 0.001 and self != s})
    
    @property
    def json_data(self):
        return {
            'system_id': self.system.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'lat': self.lat,
            'lon': self.lon,
            'routes': [r.json_data for r in self.get_routes()]
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
    
    def get_search_result(self, query):
        query = query.lower()
        number = self.number.lower()
        name = self.name.lower()
        match = 0
        if query in number:
            match += (len(query) / len(number)) * 100
            if number.startswith(query):
                match += len(query)
        elif query in name:
            match += (len(query) / len(name)) * 100
            if name.startswith(query):
                match += len(query)
            if match > 20:
                match -= 20
            else:
                match = 1
        return SearchResult('stop', self.number, self.name, f'stops/{self.number}', match)
