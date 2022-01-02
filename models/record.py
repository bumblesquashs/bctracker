
from models.system import get_system

class Record:
    def __init__(self, record_id, bus, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen):
        self.id = record_id
        self.bus = bus
        self.date = date
        self.system_id = system_id
        self.block_id = block_id
        self.routes = routes
        self.start_time = start_time
        self.end_time = end_time
        self.first_seen = first_seen
        self.last_seen = last_seen
    
    @property
    def system(self):
        return get_system(self.system_id)
    
    @property
    def is_available(self):
        return self.block is not None
    
    @property
    def block(self):
        return self.system.get_block(self.block_id)
