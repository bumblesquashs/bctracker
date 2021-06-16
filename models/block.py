
class Block:
    def __init__(self, system, block_id, service_id):
        self.system = system
        self.id = block_id
        self.service_id = service_id

        self.trips = []
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.service == other.service:
            return self.id < other.id
        else:
            return self.service < other.service

    @property
    def service(self):
        return self.system.get_service(self.service_id)

    @property
    def routes(self):
        return sorted({ trip.route for trip in self.trips })

    @property
    def routes_string(self):
        return ', '.join([ str(route.number) for route in self.routes ])
    
    @property
    def start_time(self):
        return self.trips[0].start_time
    
    @property
    def end_time(self):
        return self.trips[-1].end_time
    
    def add_trip(self, trip):
        self.trips.append(trip)