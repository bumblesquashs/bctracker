
class Position:
    def __init__(self, system, active):
        self.system = system
        self.active = active
        self.trip_id = None
        self.stop_id = None
        self.lat = None
        self.lon = None
    
    @property
    def has_location(self):
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        if self.trip_id is None or self.system is None:
            return None
        return self.system.get_trip(self.trip_id)
    
    @property
    def stop(self):
        if self.stop_id is None or self.system is None:
            return None
        return self.system.get_stop(stop_id=self.stop_id)
