
from math import sqrt

from models.service import Sheet

class Stop:
    def __init__(self, system, stop_id, number, name, lat, lon):
        self.system = system
        self.id = stop_id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
        
        self.departures = []
    
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
    
    @property
    def sheets(self):
        return {d.trip.service.sheet for d in self.departures}
    
    @property
    def default_sheet(self):
        sheets = self.sheets
        if Sheet.CURRENT in sheets:
            return Sheet.CURRENT
        if Sheet.NEXT in sheets:
            return Sheet.NEXT
        if Sheet.PREVIOUS in sheets:
            return Sheet.PREVIOUS
        return Sheet.UNKNOWN
    
    def add_departure(self, departure):
        self.departures.append(departure)
    
    def get_departures(self, sheet):
        if sheet is None:
            sheet = self.departures
        return [d for d in self.departures if d.trip.service.sheet == sheet]
    
    def get_services(self, sheet):
        return sorted({d.trip.service for d in self.get_departures(sheet)})
    
    def get_routes(self, sheet):
        return sorted({d.trip.route for d in self.get_departures(sheet)})
    
    def get_routes_string(self, sheet):
        return ', '.join([str(r.number) for r in self.get_routes(sheet)])
    
    def get_nearby_stops(self, sheet):
        stops = self.system.get_stops(sheet)
        return sorted({s for s in stops if sqrt(((self.lat - s.lat) ** 2) + ((self.lon - s.lon) ** 2)) <= 0.001 and self != s})
