
from enum import Enum

class Direction(Enum):
    OUTBOUND = 'Outbound'
    INBOUND = 'Inbound'
    UNKNOWN = 'Unknown'

class Trip:
    def __init__(self, system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign):
        self.system = system
        self.id = trip_id
        self.route_id = route_id
        self.block_id = block_id
        self.service_id = service_id
        self.shape_id = shape_id
        self.headsign = headsign

        self.stop_times = []

        if direction_id == 0:
            self.direction = Direction.OUTBOUND
        elif direction_id == 1:
            self.direction = Direction.INBOUND
        else:
            self.direction = Direction.UNKNOWN
    
    def __str__(self):
        return self.headsign
    
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
    def start_time(self):
        return self.stop_times[0].time
    
    @property
    def points(self):
        return sorted(self.system.get_shape(self.shape_id).points)

    def add_stop_time(self, stop_time):
        self.stop_times.append(stop_time)
