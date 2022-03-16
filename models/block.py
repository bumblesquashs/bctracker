
from models.service import create_service_group, create_service_groups

import realtime

class Block:
    __slots__ = ('system', 'id', 'trips', '_services', '_service_group', '_service_groups')
    
    def __init__(self, system, trip):
        self.system = system
        self.id = trip.block_id
        self.trips = [trip]
        
        self._services = None
        self._service_group = None
        self._service_groups = None
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    @property
    def services(self):
        if self._services is None:
            self._services = sorted({t.service for t in self.trips})
        return self._services
    
    @property
    def service_group(self):
        if self._service_group is None:
            self._service_group = create_service_group(self.services)
        return self._service_group
    
    @property
    def service_groups(self):
        if self._service_groups is None:
            self._service_groups = create_service_groups(self.services)
        return self._service_groups
    
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
        self._services = None
        self._service_group = None
        self._service_groups = None
        self.trips.append(trip)
    
    def get_trips(self, service_group=None):
        if service_group is None:
            return self.trips
        return [t for t in self.trips if t.service in service_group.services]
    
    def get_routes(self, service_group=None):
        return sorted({t.route for t in self.get_trips(service_group)})
    
    def get_routes_string(self, service_group=None):
        return ', '.join([r.number for r in self.get_routes(service_group)])
    
    def get_start_time(self, service_group=None):
        trips = self.get_trips(service_group)
        if len(trips) == 0:
            return None
        return trips[0].start_time
    
    def get_end_time(self, service_group=None):
        trips = self.get_trips(service_group)
        if len(trips) == 0:
            return None
        return trips[-1].end_time
    
    def get_duration(self, service_group=None):
        start_time = self.get_start_time(service_group)
        end_time = self.get_end_time(service_group)
        if start_time is None or end_time is None:
            return None
        return start_time.get_difference(end_time)
    
    def is_related(self, other):
        if self.id == other.id:
            return False
        if self.get_routes() != other.get_routes():
            return False
        if self.get_start_time() != other.get_start_time():
            return False
        if self.get_end_time() != other.get_end_time():
            return False
        return True
