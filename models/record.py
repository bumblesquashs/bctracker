
import helpers.system

from models.bus import Bus
from models.date import Date
from models.time import Time

class Record:
    '''Information about a bus' history on a specific date'''
    
    __slots__ = ('id', 'bus', 'date', 'system', 'block_id', 'route_numbers', 'start_time', 'end_time', 'first_seen', 'last_seen')
    
    @classmethod
    def from_db(cls, row, prefix='record'):
        '''Returns a record initialized from the given database row'''
        id = row[f'{prefix}_id']
        bus = Bus(row[f'{prefix}_bus_number'])
        system = helpers.system.find(row[f'{prefix}_system_id'])
        date = Date.parse_db(row[f'{prefix}_date'], system.timezone)
        block_id = row[f'{prefix}_block_id']
        route_numbers = [n.strip() for n in row[f'{prefix}_routes'].split(',')]
        start_time = Time.parse(row[f'{prefix}_start_time'], system.timezone)
        end_time = Time.parse(row[f'{prefix}_end_time'], system.timezone)
        first_seen = Time.parse(row[f'{prefix}_first_seen'], system.timezone)
        last_seen = Time.parse(row[f'{prefix}_last_seen'], system.timezone)
        return cls(id, bus, date, system, block_id, route_numbers, start_time, end_time, first_seen, last_seen)
    
    def __init__(self, id, bus, date, system, block_id, route_numbers, start_time, end_time, first_seen, last_seen):
        self.id = id
        self.bus = bus
        self.date = date
        self.system = system
        self.block_id = block_id
        self.route_numbers = route_numbers
        self.start_time = start_time
        self.end_time = end_time
        self.first_seen = first_seen
        self.last_seen = last_seen
    
    @property
    def total_seen_minutes(self):
        '''Returns the total number of minutes between when the record started and ended'''
        if self.first_seen.is_unknown or self.last_seen.is_unknown:
            return None
        first_seen = self.first_seen.get_minutes()
        if first_seen < (4 * 60):
            first_seen += (24 * 60)
        last_seen = self.last_seen.get_minutes()
        if last_seen < (4 * 60):
            last_seen += (24 * 60)
        return (last_seen - first_seen) + 1
    
    @property
    def is_suspicious(self):
        '''Checks if this record is potentially an accidental login'''
        if self.date.is_today:
            return False
        total_seen_minutes = self.total_seen_minutes
        if total_seen_minutes is None:
            return False
        return total_seen_minutes <= 5
    
    @property
    def block(self):
        '''Returns the block associated with this record'''
        return self.system.get_block(self.block_id)
    
    @property
    def is_available(self):
        '''Checks if this record has an associated block'''
        return self.block is not None
    
    @property
    def routes(self):
        if self.is_available:
            return [self.system.get_route(number=n) for n in self.route_numbers]
        return self.route_numbers
