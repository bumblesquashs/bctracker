
from models.bus import Bus
from models.date import Date
from models.system import get_system

class Transfer:
    __slots__ = ('id', 'bus', 'date', 'old_system', 'new_system')
    
    @classmethod
    def from_db(cls, row, prefix='transfer'):
        id = row[f'{prefix}_id']
        bus = Bus(row[f'{prefix}_bus_number'])
        date = Date.parse_db(row[f'{prefix}_date'])
        old_system = get_system(row[f'{prefix}_old_system_id'])
        new_system = get_system(row[f'{prefix}_new_system_id'])
        return cls(id, bus, date, old_system, new_system)
    
    def __init__(self, id, bus, date, old_system, new_system):
        self.id = id
        self.bus = bus
        self.date = date
        self.old_system = old_system
        self.new_system = new_system
