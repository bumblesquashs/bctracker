
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
    def current_trips(self):
        return [t for t in self.trips if t.service.is_current]

    @property
    def routes(self):
        return sorted({t.route for t in self.current_trips})

    @property
    def routes_string(self):
        return ', '.join([str(r.number) for r in self.routes])
    
    @property
    def start_time(self):
        return self.current_trips[0].start_time
    
    @property
    def end_time(self):
        return self.current_trips[-1].end_time
    
    def add_trip(self, trip):
        self.trips.append(trip)