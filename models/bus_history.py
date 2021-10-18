
from models.system import get_system

class BusHistory:
    def __init__(self, bus, date, system_id, feed_version, block_id, routes, start_time, end_time):
        self.bus = bus
        self.date = date
        self.system_id = system_id
        self.feed_version = feed_version
        self.block_id = block_id
        self.routes = routes
        self.start_time = start_time
        self.end_time = end_time
    
    @property
    def system(self):
        return get_system(self.system_id)
    
    @property
    def is_available(self):
        return self.block is not None
    
    @property
    def block(self):
        return self.system.get_block(self.block_id)
    
    @property
    def json_data(self):
        return {
            'bus_number': self.bus.number,
            'date': self.date.strftime('%Y-%m-%d'),
            'system_id': self.system_id,
            'feed_version': self.feed_version,
            'block_id': self.block_id,
            'routes': self.routes,
            'start_time': self.start_time.full_string,
            'end_time': self.end_time.full_string
        }
