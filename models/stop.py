
from math import sqrt

class Stop:
    def __init__(self, system, stop_id, number, name, lat, lon):
        self.system = system
        self.id = stop_id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
        
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
        return sorted({d.trip.service for d in self.departures if d.trip.service.is_current})
    
    @property
    def routes(self):
        routes = sorted({d.trip.route for d in self.departures})
        current_routes = [r for r in routes if r.is_current]
        if len(current_routes) == 0:
            return routes
        return current_routes
    
    @property
    def routes_string(self):
        return ', '.join([str(r.number) for r in self.routes])
    
    @property
    def nearby_stops(self):
        stops = self.system.all_stops()
        return sorted({s for s in stops if sqrt(((self.lat - s.lat) ** 2) + ((self.lon - s.lon) ** 2)) <= 0.001 and self != s})
    
    @property
    def json_data(self):
        return {
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'lat': self.lat,
            'lon': self.lon
        }
    
    def add_departure(self, departure):
        self.departures.append(departure)
