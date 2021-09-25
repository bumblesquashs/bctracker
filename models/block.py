
import formatting
import realtime

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
    def available_trips(self):
        if self.is_current:
            return [t for t in self.trips if t.service.is_current]
        else:
            return self.trips
    
    @property
    def routes(self):
        return sorted({t.route for t in self.available_trips})
    
    @property
    def routes_string(self):
        return ', '.join([str(r.number) for r in self.routes])
    
    @property
    def start_time(self):
        return self.available_trips[0].start_time
    
    @property
    def end_time(self):
        return self.available_trips[-1].end_time

    @property
    def duration(self):
    	return formatting.duration_between_timestrs(self.start_time, self.end_time)
    
    @property
    def positions(self):
        positions = realtime.get_positions()
        return [p for p in positions if p.system == self.system and p.trip is not None and p.trip.block_id == self.id]
    
    def add_trip(self, trip):
        self.trips.append(trip)
