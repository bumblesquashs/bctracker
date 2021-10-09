
from math import sqrt

class Stop:
    def __init__(self, system, stop_id, number, name, lat, lon):
        self.system = system
        self.id = stop_id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
        
        self.stop_times = []
    
    def __hash__(self):
        return hash(self.id)
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.name == other.name:
            return self.number < other.number
        return self.name < other.name
    
    def add_stop_time(self, stop_time):
        self.stop_times.append(stop_time)
    
    def get_stop_times(self, sheet):
        if sheet is None:
            return self.stop_times
        return [s for s in self.stop_times if s.trip.service.sheet == sheet]
    
    def get_services(self, sheet):
        return sorted({s.trip.service for s in self.get_stop_times(sheet)})
    
    def get_routes(self, sheet):
        return sorted({s.trip.route for s in self.get_stop_times(sheet)})
    
    def get_routes_string(self, sheet):
        return ', '.join([str(r.number) for r in self.get_routes(sheet)])
    
    def get_nearby_stops(self):
        stops = self.system.all_stops()
        return sorted({s for s in stops if sqrt(((self.lat - s.lat) ** 2) + ((self.lon - s.lon) ** 2)) <= 0.001 and self != s})
