
import helpers.system

from models.bus import Bus
from models.date import Date
from models.time import Time

class Record:
    '''Information about a bus' history on a specific date'''
    
    __slots__ = (
        'id',
        'bus',
        'date',
        'system',
        'block_id',
        'route_numbers',
        'start_time',
        'end_time',
        'first_seen',
        'last_seen',
        'warnings'
    )
    
    @classmethod
    def from_db(cls, row, prefix='record'):
        '''Returns a record initialized from the given database row'''
        id = row[f'{prefix}_id']
        system = helpers.system.find(row[f'{prefix}_system_id'])
        agency = system.agency
        bus = Bus.find(agency, row[f'{prefix}_bus_number'])
        date = Date.parse(row[f'{prefix}_date'], system.timezone)
        block_id = row[f'{prefix}_block_id']
        route_numbers = [n.strip() for n in row[f'{prefix}_routes'].split(',')]
        timezone = system.timezone
        accurate_seconds = system.agency.accurate_seconds
        start_time = Time.parse(row[f'{prefix}_start_time'], timezone, accurate_seconds)
        end_time = Time.parse(row[f'{prefix}_end_time'], timezone, accurate_seconds)
        first_seen = Time.parse(row[f'{prefix}_first_seen'], timezone, accurate_seconds)
        last_seen = Time.parse(row[f'{prefix}_last_seen'], timezone, accurate_seconds)
        return cls(id, bus, date, system, block_id, route_numbers, start_time, end_time, first_seen, last_seen)
    
    @property
    def total_minutes(self):
        '''Returns the total length of the record's block'''
        if self.start_time.is_unknown or self.end_time.is_unknown:
            return None
        return (self.end_time.get_minutes() - self.start_time.get_minutes()) + 1
    
    @property
    def total_seen_minutes(self):
        '''Returns the total number of minutes between when the record started and ended'''
        if self.first_seen.is_unknown or self.last_seen.is_unknown:
            return None
        return (self.last_seen.get_minutes() - self.first_seen.get_minutes()) + 1
    
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
        self.warnings = []
        
        total_minutes = self.total_minutes
        total_seen_minutes = self.total_seen_minutes
        if total_minutes is not None and total_seen_minutes is not None:
            if not date.is_today and (total_seen_minutes / total_minutes) < 0.1 and total_seen_minutes <= 10:
                if total_seen_minutes == 1:
                    self.warnings.append('Bus was logged in for only 1 minute')
                else:
                    self.warnings.append(f'Bus was logged in for only {total_seen_minutes} minutes')
            if (start_time.get_minutes() - last_seen.get_minutes()) > 30:
                self.warnings.append('Bus was logged in before block started')
            if (first_seen.get_minutes() - end_time.get_minutes()) > 30:
                self.warnings.append('Bus was logged in after block ended')
