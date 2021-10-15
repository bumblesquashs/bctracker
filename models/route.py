import realtime

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
    def is_current(self):
        for trip in self.trips:
            if trip.service.is_current:
                return True
        return False
    
    @property
    def services(self):
        if self.is_current:
            return sorted({ t.service for t in self.trips if t.service.is_current })
        else:
            return sorted({ t.service for t in self.trips })
    
    @property
    def headsigns(self):
        if self.is_current:
            return sorted({ str(t) for t in self.trips if t.service.is_current })
        else:
            return sorted({ str(t) for t in self.trips })
    
    @property
    def positions(self):
        positions = realtime.get_positions()
        return [p for p in positions if p.system == self.system and p.trip is not None and p.trip.route_id == self.id]
    
    def add_trip(self, trip):
        self.trips.append(trip)
