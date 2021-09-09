
class Route:
    def __init__(self, system, route_id, number, name, colour):
        self.system = system
        self.id = route_id
        self.number = number
        self.name = name
        self.colour = colour
        
        self.trips = []
    
    def __str__(self):
        return f'{self.number} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.number < other.number
    
    def __gt__(self, other):
        return self.number > other.number
    
    @property
    def sheets(self):
        return {t.service.sheet for t in self.trips}
    
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
