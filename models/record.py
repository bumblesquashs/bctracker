
from models.bus import Bus
from models.system import get_system
from models.time import Time

import formatting

class Record:
    def __init__(self, row, prefix='record'):
        self.id = row[f'{prefix}_id']
        self.bus = Bus(row[f'{prefix}_bus_number'])
        self.date = formatting.database(row[f'{prefix}_date'])
        self.system_id = row[f'{prefix}_system_id']
        self.block_id = row[f'{prefix}_block_id']
        self.routes = row[f'{prefix}_routes']
        self.start_time = Time(row[f'{prefix}_start_time'])
        self.end_time = Time(row[f'{prefix}_end_time'])
        self.first_seen = Time(row[f'{prefix}_first_seen'])
        self.last_seen = Time(row[f'{prefix}_last_seen'])
    
    @property
    def system(self):
        return get_system(self.system_id)
    
    @property
    def is_available(self):
        return self.block is not None
    
    @property
    def block(self):
        return self.system.get_block(self.block_id)
