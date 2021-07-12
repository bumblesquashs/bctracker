
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
    
    @property
    def services(self):
        return sorted({ s.trip.service for s in self.stop_times if s.trip.service.is_current })
    
    @property
    def routes(self):
        return sorted({ s.trip.route for s in self.stop_times })
    
    def add_stop_time(self, stop_time):
        self.stop_times.append(stop_time)
