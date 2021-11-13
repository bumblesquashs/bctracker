
from models.service import Sheet
import realtime

class Block:
    def __init__(self, system, block_id):
        self.system = system
        self.id = block_id
        
        self.trips = []
        self._sheets = None
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    @property
    def sheets(self):
        if self._sheets is None:
            self._sheets = {t.service.sheet for t in self.trips}
        return self._sheets
    
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
        return [p for p in positions if p.system == self.system and p.trip is not None and p.trip.block_id == self.id]
    
    def add_trip(self, trip):
        self.trips.append(trip)
        self._sheets = None
    
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
            return None
        else:
            return trips[0].start_time
    
    def get_end_time(self, sheet):
        trips = self.get_trips(sheet)
        if not trips:
            return None
        else:
            return trips[-1].end_time
    
    def get_duration(self, sheet):
        start_time = self.get_start_time(sheet)
        end_time = self.get_end_time(sheet)
        if start_time is None or end_time is None:
            return 0
        return start_time.get_difference(end_time)
    
    def get_related_blocks(self, sheet):
        related_blocks = [b for b in self.system.get_blocks(sheet) if self.is_related(b, sheet)]
        related_blocks.sort(key=lambda b: b.get_services(sheet)[0])
        return related_blocks
    
    def is_related(self, other, sheet):
        if self.id == other.id:
            return False
        if sheet not in other.sheets:
            return False
        if self.get_routes(sheet) != other.get_routes(sheet):
            return False
        if self.get_start_time(sheet) != other.get_start_time(sheet):
            return False
        if self.get_end_time(sheet) != other.get_end_time(sheet):
            return False
        return True
