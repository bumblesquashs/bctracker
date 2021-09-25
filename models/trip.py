from datetime import datetime

import formatting
import realtime

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
    def duration(self):
        return formatting.duration_between_timestrs(self.start_time, self.end_time)
    
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
    
    @property
    def positions(self):
        positions = realtime.get_positions()
        return [p for p in positions if p.system == self.system and p.trip_id == self.id]
    
    def add_stop_time(self, stop_time):
        self.stop_times.append(stop_time)
    
    def get_stop_time(self, stop):
        stop_times = [s for s in self.stop_times if s.stop == stop]
        if len(stop_times) == 0:
            return None
        if len(stop_times) == 1:
            return stop_times[0]
        now = datetime.now()
        current_mins = formatting.get_minutes(now.hour, now.minute)
        stop_times.sort(key=lambda s: abs(current_mins - s.get_time_minutes()))
        return stop_times[0]
    
    def get_previous_stop(self, stop_time):
        for other_st in self.stop_times:
            if other_st.sequence == (stop_time.sequence - 1):
                return other_st.stop
        return None
