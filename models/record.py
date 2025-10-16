
from dataclasses import dataclass, field

from models.context import Context
from models.date import Date
from models.row import Row
from models.time import Time
from models.vehicle import Vehicle

@dataclass(slots=True)
class Record:
    '''Information about a vehicle's history on a specific date'''
    
    id: int
    allocation_id: int
    context: Context
    vehicle: Vehicle
    date: Date
    block_id: str
    route_numbers: list[str]
    start_time: Time
    end_time: Time
    first_seen: Time
    last_seen: Time
    
    warnings: list[str] = field(default_factory=list, init=False)
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a record initialized from the given database row'''
        id = row['id']
        allocation_id = row['allocation_id']
        context = row.context()
        vehicle = context.find_vehicle(row['vehicle_id'])
        date = Date.parse(row['date'], context.timezone)
        block_id = row['block_id']
        if 'route_numbers' in row:
            route_numbers = [n.strip() for n in row['route_numbers'].split(',')]
        else:
            route_numbers = []
        start_time = Time.parse(row['start_time'], context.timezone, context.accurate_seconds)
        end_time = Time.parse(row['end_time'], context.timezone, context.accurate_seconds)
        first_seen = Time.parse(row['first_seen'], context.timezone, context.accurate_seconds)
        last_seen = Time.parse(row['last_seen'], context.timezone, context.accurate_seconds)
        return cls(id, allocation_id, context, vehicle, date, block_id, route_numbers, start_time, end_time, first_seen, last_seen)
    
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
        return self.context.system.get_block(self.block_id)
    
    @property
    def is_available(self):
        '''Checks if this record has an associated block'''
        return self.block is not None
    
    @property
    def routes(self):
        if self.is_available:
            return [self.context.system.get_route(number=n) for n in self.route_numbers]
        return self.route_numbers
    
    def __post_init__(self):
        total_minutes = self.total_minutes
        total_seen_minutes = self.total_seen_minutes
        if total_minutes is not None and total_seen_minutes is not None:
            if not self.date.is_today and (total_seen_minutes / total_minutes) < 0.1 and total_seen_minutes <= 10:
                if total_seen_minutes == 1:
                    self.warnings.append(f'{self.vehicle.type_generic_name} was logged in for only 1 minute')
                else:
                    self.warnings.append(f'{self.vehicle.type_generic_name} was logged in for only {total_seen_minutes} minutes')
            if (self.start_time.get_minutes() - self.last_seen.get_minutes()) > 30:
                self.warnings.append(f'{self.vehicle.type_generic_name} was logged in before block started')
            if (self.first_seen.get_minutes() - self.end_time.get_minutes()) > 30:
                self.warnings.append(f'{self.vehicle.type_generic_name} was logged in after block ended')
