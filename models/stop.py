
class Stop:
    def __init__(self, system, stop_id, number, name, lat, lon):
        self.system = system
        self.id = stop_id
        self.number = number
        self.name = name
        self.lat = lat
        self.lon = lon
        
        self.stop_times = []
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.id == other.id
    
    def add_stop_time(self, stop_time):
        self.stop_times.append(stop_time)
    
    def get_stop_times(self, sheet):
        if sheet is None:
            return self.stop_times
        return [s for s in self.stop_times if s.trip.service.sheet == sheet]
    
    def get_services(self, sheet):
        return sorted({s.trip.service for s in self.get_stop_times(sheet)})
    
    def get_soutes(self, sheet):
        return sorted({s.trip.route for s in self.get_stop_times(sheet)})
