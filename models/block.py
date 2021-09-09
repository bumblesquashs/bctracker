
class Block:
    def __init__(self, system, block_id):
        self.system = system
        self.id = block_id
        
        self.trips = []
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
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
    
    def get_routes(self, sheet):
        return sorted({t.route for t in self.get_trips(sheet)})
    
    def get_routes_string(self, sheet):
        return ', '.join([str(r.number) for r in self.get_routes(sheet)])
    
    def get_start_time(self, sheet):
        trips = self.get_trips(sheet)
        if not trips:
            return 'N/A'
        else:
            return trips[0].start_time
    
    def get_end_time(self, sheet):
        trips = self.get_trips(sheet)
        if not trips:
            return 'N/A'
        else:
            return trips[-1].end_time
