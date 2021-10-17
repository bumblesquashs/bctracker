import realtime

from models.service import Sheet

class Route:
    def __init__(self, system, route_id, number, name, colour):
        self.system = system
        self.id = route_id
        self.number = number
        self.name = name
        self.colour = colour
        
        self.number_value = int(''.join([d for d in number if d.isdigit()]))
        
        self.trips = []
    
    def __str__(self):
        return f'{self.number} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.number_value < other.number_value
    
    def __gt__(self, other):
        return self.number_value > other.number_value
    
    @property
    def sheets(self):
        return {t.service.sheet for t in self.trips}
    
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
    
    @property
    def positions(self):
        positions = realtime.get_positions()
        return [p for p in positions if p.system == self.system and p.trip is not None and p.trip.route_id == self.id]
    
    def add_trip(self, trip):
        self.trips.append(trip)
    
    def get_trips(self, sheet):
        if sheet is None:
            return self.trips
        return [t for t in self.trips if t.service.sheet == sheet]
    
    def get_services(self, sheet):
        return sorted({t.service for t in self.get_trips(sheet)})
    
    def get_headsigns(self, sheet):
        return sorted({str(t) for t in self.get_trips(sheet)})
