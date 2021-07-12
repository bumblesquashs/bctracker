from models.system import get_system
from realtime import get_bus

class BusHistory:
    def __init__(self, date, bus_id, number, system_id, feed_version, block_id, routes):
        self.date = date
        self.bus_id = bus_id
        self.number = number
        self.system_id = system_id
        self.feed_version = feed_version
        self.block_id = block_id
        self.routes = routes
    
    def __eq__(self, other):
        return self.bus == other.bus
    
    def __lt__(self, other):
        return self.bus < other.bus
    
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
    def routes_string(self):
        return ', '.join([ str(r) for r in self.routes ])
    
    @property
    def bus(self):
        return get_bus(number=self.number)
    
    @property
    def json_data(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'bus_id': self.bus_id,
            'number': self.number,
            'system_id': self.system_id,
            'feed_version': self.feed_version,
            'block_id': self.block_id,
            'routes': self.routes
        }