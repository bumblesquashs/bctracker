from datetime import datetime

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
        
        self.departures = []
        self._direction = None
        self._related_trips = None
    
    def __str__(self):
        if self.headsign.startswith(str(self.route.number)):
            return self.headsign
        return f'{self.route.number} {self.headsign}'
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.first_departure < other.first_departure
    
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
    def first_departure(self):
        return self.departures[0]
    
    @property
    def last_departure(self):
        return self.departures[-1]
    
    @property
    def duration(self):
        return self.first_departure.time.get_difference(self.last_departure.time)
    
    @property
    def points(self):
        return sorted(self.system.get_shape(self.shape_id).points)
    
    @property
    def direction(self):
        if self._direction is None:
            first_stop = self.first_departure.stop
            last_stop = self.last_departure.stop
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
    
    @property
    def related_trips(self):
        if self._related_trips is None:
            self._related_trips = [t for t in self.system.get_trips(self.service.sheet) if self.is_related(t)]
            self._related_trips.sort(key=lambda t: t.service)
        return self._related_trips
    
    def add_departure(self, departure):
        self.departures.append(departure)
    
    def get_departure(self, stop):
        departures = [d for d in self.departures if d.stop == stop]
        if len(departures) == 0:
            return None
        if len(departures) == 1:
            return departures[0]
        now = datetime.now()
        current_mins = (now.hour * 60) + now.minute
        departures.sort(key=lambda d: abs(current_mins - d.time.get_minutes()))
        return departures[0]
    
    def get_previous_departure(self, departure):
        for other_departure in self.departures:
            if other_departure.sequence == (departure.sequence - 1):
                return other_departure
        return None
    
    def is_related(self, other):
        if self.id == other.id:
            return False
        if self.service.sheet != other.service.sheet:
            return False
        if self.route_id != other.route_id:
            return False
        if self.first_departure.time != other.first_departure.time:
            return False
        if self.last_departure.time != other.last_departure.time:
            return False
        if self.direction_id != other.direction_id:
            return False
        return True
