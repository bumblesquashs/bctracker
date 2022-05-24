
from models.bus import Bus
from models.system import get_system

import formatting

class Transfer:
    __slots__ = ('id', 'bus', 'date', 'old_system_id', 'new_system_id')
    
    def __init__(self, row, prefix='transfer'):
        self.id = row[f'{prefix}_id']
        self.bus = Bus(row[f'{prefix}_bus_number'])
        self.date = formatting.database(row[f'{prefix}_date'])
        self.old_system_id = row[f'{prefix}_old_system_id']
        self.new_system_id = row[f'{prefix}_new_system_id']
    
    @property
    def old_system(self):
        return get_system(self.old_system_id)
    
    @property
    def new_system(self):
        return get_system(self.new_system_id)
