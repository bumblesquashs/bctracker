
import helpers.system

from models.bus import Bus
from models.date import Date

class Assignment:
    
    __slots__ = (
        'system_id',
        'block_id',
        'bus_number',
        'date'
    )
    
    @classmethod
    def from_db(cls, row, prefix='assignment'):
        system_id = row[f'{prefix}_system_id']
        block_id = row[f'{prefix}_block_id']
        bus_number = row[f'{prefix}_bus_number']
        date = Date.parse(row[f'{prefix}_date'])
        return cls(system_id, block_id, bus_number, date)
    
    @property
    def key(self):
        return (self.system_id, self.block_id)
    
    @property
    def bus(self):
        system = helpers.system.find(self.system_id)
        return Bus.find(system.agency, self.bus_number)
    
    def __init__(self, system_id, block_id, bus_number, date):
        self.system_id = system_id
        self.block_id = block_id
        self.bus_number = bus_number
        self.date = date
