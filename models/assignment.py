
from models.bus import Bus
from models.context import Context
from models.date import Date

class Assignment:
    '''An association between a block and a bus for a specific date'''
    
    __slots__ = (
        'context',
        'block_id',
        'bus_number',
        'date'
    )
    
    @classmethod
    def from_db(cls, row, prefix='assignment'):
        '''Returns an assignment initialized from the given database row'''
        context = Context.find(system_id=row[f'{prefix}_system_id'])
        block_id = row[f'{prefix}_block_id']
        bus_number = row[f'{prefix}_bus_number']
        date = Date.parse(row[f'{prefix}_date'], context.timezone)
        return cls(context, block_id, bus_number, date)
    
    @property
    def key(self):
        '''The unique identifier for this assignment'''
        return (self.context.system_id, self.block_id)
    
    @property
    def bus(self):
        '''The bus for this assignment'''
        return Bus.find(self.context, self.bus_number)
    
    def __init__(self, context: Context, block_id, bus_number, date):
        self.context = context
        self.block_id = block_id
        self.bus_number = bus_number
        self.date = date
