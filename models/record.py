
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass, field

from models.bus import Bus
from models.date import Date
from models.row import Row
from models.time import Time

@dataclass(slots=True)
class Record:
    '''Information about a bus' history on a specific date'''
    
    system: System
    id: int
    bus: Bus
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
        context = row.context()
        id = row['id']
        bus = context.find_bus(row['bus_number'])
        date = Date.parse(row['date'], context.timezone)
        block_id = row['block_id']
        route_numbers = [n.strip() for n in row['routes'].split(',')]
        start_time = Time.parse(row['start_time'], context.timezone, context.accurate_seconds)
        end_time = Time.parse(row['end_time'], context.timezone, context.accurate_seconds)
        first_seen = Time.parse(row['first_seen'], context.timezone, context.accurate_seconds)
        last_seen = Time.parse(row['last_seen'], context.timezone, context.accurate_seconds)
        return cls(context.system, id, bus, date, block_id, route_numbers, start_time, end_time, first_seen, last_seen)
    
    @property
    def context(self):
        '''The context for this record'''
        return self.system.context
    
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
    
    def __post_init__(self):
        total_minutes = self.total_minutes
        total_seen_minutes = self.total_seen_minutes
        if total_minutes is not None and total_seen_minutes is not None:
            if not self.date.is_today and (total_seen_minutes / total_minutes) < 0.1 and total_seen_minutes <= 10:
                if total_seen_minutes == 1:
                    self.warnings.append('Bus was logged in for only 1 minute')
                else:
                    self.warnings.append(f'Bus was logged in for only {total_seen_minutes} minutes')
            if (self.start_time.get_minutes() - self.last_seen.get_minutes()) > 30:
                self.warnings.append('Bus was logged in before block started')
            if (self.first_seen.get_minutes() - self.end_time.get_minutes()) > 30:
                self.warnings.append('Bus was logged in after block ended')
