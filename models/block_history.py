from models.system import get_system

class BlockHistory:
    def __init__(self, date, system_id, feed_version, block_id, routes_string, start_time, end_time):
        self.date = date
        self.system_id = system_id
        self.feed_version = feed_version
        self.block_id = block_id
        self.routes_string = routes_string
        self.start_time = start_time
        self.end_time = end_time
    
    def __eq__(self, other):
        return self.block_id == other.block_id
    
    def __lt__(self, other):
        if self.date == other.date:
            return self.start_time > other.start_time
        return self.date > other.date
    
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
            'date': self.date.strftime('%Y-%m-%d'),
            'system_id': self.system_id,
            'feed_version': self.feed_version,
            'block_id': self.block_id,
            'routes': self.routes_string,
            'start_time': self.start_time.full_string,
            'end_time': self.end_time.full_string
        }
