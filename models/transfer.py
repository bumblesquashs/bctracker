
from dataclasses import dataclass

from models.bus import Bus
from models.context import Context
from models.date import Date

@dataclass(slots=True)
class Transfer:
    '''Information about a bus moving from one system to another system'''
    
    id: int
    bus: Bus
    date: Date
    old_context: Context
    new_context: Context
    
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
