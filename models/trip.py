from datetime import datetime

import realtime

class Trip:
    def __init__(self, system, row):
        self.system = system
        self.id = row['trip_id']
        self.route_id = row['route_id']
        self.service_id = row['service_id']
        self.block_id = row['block_id']
        self.direction_id = int(row['direction_id'])
        self.shape_id = row['shape_id']
        self.headsign = row['trip_headsign']
        
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
    def stops(self):
        return {d.stop for d in self.departures}
    
    @property
    def first_departure(self):
        return self.departures[0]
    
    @property
    def last_departure(self):
        return self.departures[-1]
    
    @property
    def start_time(self):
        return self.first_departure.time
    
    @property
    def end_time(self):
        return self.last_departure.time
    
    @property
    def duration(self):
        return self.start_time.get_difference(self.end_time)
    
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
    def positions(self):
        positions = realtime.get_positions()
        return [p for p in positions if p.system == self.system and p.trip_id == self.id]
    
    @property
    def related_trips(self):
        if self._related_trips is None:
            self._related_trips = [t for t in self.system.get_trips(self.service.sheet) if self.is_related(t)]
            self._related_trips.sort(key=lambda t: t.service)
        return self._related_trips
    
    @property
    def json_data(self):
        return {
            'shape_id': self.shape_id,
            'colour': self.route.colour,
            'points': [p.json_data for p in self.points]
        }
    
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
        for previous_departure in self.departures:
            if previous_departure.sequence == (departure.sequence - 1):
                return previous_departure
        return None
    
    def is_related(self, other):
        if self.id == other.id:
            return False
        if self.service.sheet != other.service.sheet:
            return False
        if self.route_id != other.route_id:
            return False
        if self.start_time != other.start_time:
            return False
        if self.end_time != other.end_time:
            return False
        if self.direction_id != other.direction_id:
            return False
        return True
