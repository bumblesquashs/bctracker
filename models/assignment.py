
from dataclasses import dataclass

from models.bus import Bus
from models.context import Context
from models.date import Date
from models.row import Row

@dataclass(slots=True)
class Assignment:
    '''An association between a block and a bus for a specific date'''
    
    context: Context
    block_id: str
    bus_number: int
    date: Date
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns an assignment initialized from the given database row'''
        context = row.context()
        block_id = row['block_id']
        bus_number = row['bus_number']
        date = Date.parse(row['date'], context.timezone)
        return cls(context, block_id, bus_number, date)
    
    @property
    def key(self):
        '''The unique identifier for this assignment'''
        return (self.context.system_id, self.block_id)
    
    @property
    def bus(self):
        '''The bus for this assignment'''
        return Bus.find(self.context, self.bus_number)
