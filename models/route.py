
class Route:
    def __init__(self, system, route_id, number, name):
        self.system = system
        self.route_id = route_id
        self.number = number
        self.name = name

        self.trips = []
    
    def __str__(self):
        return f'{self.number} {self.name}'
    
    def __hash__(self):
        return hash(self.route_id)
    
    def __eq__(self, other):
        return self.route_id == other.route_id
    
    def __lt__(self, other):
        return self.number < other.number
    
    def __gt__(self, other):
        return self.number > other.number
    
    @property
    def services(self):
        return set(map(lambda t: t.service, self.trips))
    
    def add_trip(self, trip):
        self.trips.append(trip)
