
from models.bus import Bus
from models.date import Date
from models.time import Time

import queries.systems

class Record:
    '''Information about a bus' history on a specific date'''
    
    __slots__ = ('id', 'bus', 'date', 'system', 'block_id', 'routes', 'start_time', 'end_time', 'first_seen', 'last_seen')
    
    @classmethod
    def from_db(cls, row, prefix='record'):
        record_id = row[f'{prefix}_id']
        bus = Bus(row[f'{prefix}_bus_number'])
        date = Date.parse_db(row[f'{prefix}_date'])
        system = queries.systems.find(row[f'{prefix}_system_id'])
        block_id = row[f'{prefix}_block_id']
        routes = row[f'{prefix}_routes']
        start_time = Time.parse(row[f'{prefix}_start_time'])
        end_time = Time.parse(row[f'{prefix}_end_time'])
        first_seen = Time.parse(row[f'{prefix}_first_seen'])
        last_seen = Time.parse(row[f'{prefix}_last_seen'])
        return cls(record_id, bus, date, system, block_id, routes, start_time, end_time, first_seen, last_seen)
    
    def __init__(self, record_id, bus, date, system, block_id, routes, start_time, end_time, first_seen, last_seen):
        self.id = record_id
        self.bus = bus
        self.date = date
        self.system = system
        self.block_id = block_id
        self.routes = routes
        self.start_time = start_time
        self.end_time = end_time
        self.first_seen = first_seen
        self.last_seen = last_seen
    
    @property
    def block(self):
        return self.system.get_block(self.block_id)
    
    @property
    def is_available(self):
        return self.block is not None
