
class Trip:
    def __init__(self, system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign):
        self.system = system
        self.id = trip_id
        self.route_id = route_id
        self.block_id = block_id
        self.direction_id = direction_id
        self.service_id = service_id
        self.shape_id = shape_id
        self.headsign = headsign

        self.stop_times = []
        self._direction = None
    
    def __str__(self):
        if self.headsign.startswith(str(self.route.number)):
            return self.headsign
        return f'{self.route.number} {self.headsign}'
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.stop_times[0] < other.stop_times[0]
    
    @property
    def route(self):
        return self.system.get_route(route_id=self.route_id)
    
    @property
    def block(self):
        return self.system.get_block(self.block_id)
    
    @property
    def service(self):
        return self.system.get_service(self.service_id)
    
    @property
    def first_stop(self):
        return self.stop_times[0]

    @property
    def last_stop(self):
        return self.stop_times[-1]
    
    @property
    def start_time(self):
        return self.first_stop.time
    
    @property
    def end_time(self):
        return self.last_stop.time
    
    @property
    def points(self):
        return sorted(self.system.get_shape(self.shape_id).points)
    
    @property
    def direction(self):
        if self._direction is None:
            first_stop = self.first_stop.stop
            last_stop = self.last_stop.stop
            lat_diff = first_stop.lat - last_stop.lat
            lon_diff = first_stop.lon - last_stop.lon
            if lat_diff == 0 and lon_diff == 0:
                self._direction = 'Circular'
            elif abs(lat_diff) > abs(lon_diff):
                self._direction = 'Southbound' if lat_diff > 0 else 'Northbound'
            elif abs(lon_diff) > abs(lat_diff):
                self._direction = 'Westbound' if lon_diff > 0 else 'Eastbound'
            else:
                self._direction = ''
        return self._direction

    def add_stop_time(self, stop_time):
        self.stop_times.append(stop_time)
