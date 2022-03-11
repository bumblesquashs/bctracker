
from math import sqrt

from models.search_result import SearchResult
from models.time import get_current_minutes

class Stop:
    __slots__ = ('system', 'id', 'number', 'name', 'lat', 'lon', 'departures')
    
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
        return sorted({d.trip.service for d in self.departures})
    
    @property
    def routes(self):
        return sorted({d.trip.route for d in self.departures})
    
    @property
    def routes_string(self):
        return ', '.join([r.number for r in self.routes])
    
    @property
    def nearby_stops(self):
        stops = self.system.get_stops()
        return sorted({s for s in stops if sqrt(((self.lat - s.lat) ** 2) + ((self.lon - s.lon) ** 2)) <= 0.001 and self != s})
    
    @property
    def upcoming_departures(self):
        current_mins = get_current_minutes()
        return [d for d in self.departures if d.trip.service.is_today and current_mins <= d.time.get_minutes() <= current_mins + 30]
    
    @property
    def json_data(self):
        return {
            'system_id': self.system.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'lat': self.lat,
            'lon': self.lon,
            'routes': [r.json_data for r in self.routes]
        }
    
    def add_departure(self, departure):
        self.departures.append(departure)
    
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
