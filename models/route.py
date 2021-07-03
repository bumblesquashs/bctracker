
class Route:
    def __init__(self, system, route_id, number, name):
        self.system = system
        self.id = route_id
        self.number = number
        self.name = name

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
    def services(self):
        return sorted({ t.service for t in self.trips if t.service.is_current })
    
    @property
    def is_current(self):
        for service in self.services:
            if service.is_current:
                return True
        return False
    
    @property
    def headsigns(self):
        return sorted({ str(t) for t in self.trips if t.service.is_current })
    
    def add_trip(self, trip):
        self.trips.append(trip)
