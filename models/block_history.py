from models.system import get_system
from formatting import format_time

class BlockHistory:
    def __init__(self, date, system_id, feed_version, block_id, routes, start_time, end_time):
        self.date = date
        self.system_id = system_id
        self.feed_version = feed_version
        self.block_id = block_id
        self.routes = routes
        self.start_time = format_time(start_time)
        self.end_time = format_time(end_time)
    
    def __eq__(self, other):
        return self.block_id == other.block_id
    
    def __lt__(self, other):
        if self.date == other.date:
            (sh, sm) = self.start_time.split(':')
            (oh, om) = other.start_time.split(':')
            if sh == oh:
                return int(sm) > int(om)
            else:
                return int(sh) > int(oh)
        return self.date > other.date
    
    @property
    def system(self):
        return get_system(self.system_id)
    
    @property
    def is_current(self):
        return self.feed_version == self.system.feed_version or (self.block is not None and self.block.is_current)
    
    @property
    def block(self):
        return self.system.get_block(self.block_id)

    @property
    def routes_string(self):
        return ', '.join([ str(r) for r in self.routes ])
    
    @property
    def json_data(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'system_id': self.system_id,
            'feed_version': self.feed_version,
            'block_id': self.block_id,
            'routes': self.routes,
            'start_time': self.start_time,
            'end_time': self.end_time
        }