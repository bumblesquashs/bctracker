
import realtime

class Block:
    __slots__ = ('system', 'id', 'trips')
    
    def __init__(self, system, trip):
        self.system = system
        self.id = trip.block_id
        self.trips = [trip]
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    @property
    def services(self):
        return sorted({t.service for t in self.trips})
    
    @property
    def routes(self):
        return sorted({t.route for t in self.trips})
    
    @property
    def routes_string(self):
        return ', '.join([r.number for r in self.routes])
    
    @property
    def start_time(self):
        if len(self.trips) == 0:
            return None
        return self.trips[0].start_time
    
    @property
    def end_time(self):
        if len(self.trips) == 0:
            return None
        return self.trips[-1].end_time
    
    @property
    def duration(self):
        start_time = self.start_time
        end_time = self.end_time
        if start_time is None or end_time is None:
            return None
        return start_time.get_difference(end_time)
    
    @property
    def related_blocks(self):
        related_blocks = [b for b in self.system.get_blocks() if self.is_related(b)]
        related_blocks.sort(key=lambda b: b.services[0])
        return related_blocks
    
    @property
    def positions(self):
        positions = realtime.get_positions()
        return [p for p in positions if p.system == self.system and p.trip is not None and p.trip.block_id == self.id]
    
    def add_trip(self, trip):
        self.trips.append(trip)
    
    def is_related(self, other):
        if self.id == other.id:
            return False
        if self.routes != other.routes:
            return False
        if self.start_time != other.start_time:
            return False
        if self.end_time != other.end_time:
            return False
        return True
