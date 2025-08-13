
from dataclasses import dataclass

from models.context import Context
from models.date import Date
from models.row import Row

@dataclass(slots=True)
class Assignment:
    '''An association between a block and a bus for a specific date'''
    
    block_id: str
    allocation_id: int
    context: Context
    vehicle_id: str
    date: Date
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns an assignment initialized from the given database row'''
        context = row.context()
        block_id = row['block_id']
        allocation_id = row['allocation_id']
        vehicle_id = row['vehicle_id']
        date = Date.parse(row['date'], context.timezone)
        return cls(block_id, allocation_id, context, vehicle_id, date)
    
    @property
    def bus(self):
        '''The bus for this assignment'''
        return self.context.find_bus(self.vehicle_id)
