
from models.bus import Bus
from models.context import Context
from models.date import Date

class Transfer:
    '''Information about a bus moving from one system to another system'''
    
    __slots__ = (
        'id',
        'bus',
        'date',
        'old_context',
        'new_context'
    )
    
    @classmethod
    def from_db(cls, row, prefix='transfer'):
        '''Returns a transfer initialized from the given database row'''
        id = row[f'{prefix}_id']
        context = Context.find(agency_id='bc-transit')
        bus = Bus.find(context, row[f'{prefix}_bus_number'])
        old_context = Context.find(system_id=row[f'{prefix}_old_system_id'])
        new_context = Context.find(system_id=row[f'{prefix}_new_system_id'])
        date = Date.parse(row[f'{prefix}_date'], new_context.timezone)
        return cls(id, bus, date, old_context, new_context)
    
    def __init__(self, id, bus, date, old_context: Context, new_context: Context):
        self.id = id
        self.bus = bus
        self.date = date
        self.old_context = old_context
        self.new_context = new_context
