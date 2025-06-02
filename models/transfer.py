
from dataclasses import dataclass

from models.bus import Bus
from models.context import Context
from models.date import Date
from models.row import Row

@dataclass(slots=True)
class Transfer:
    '''Information about a bus moving from one system to another system'''
    
    id: int
    bus: Bus
    date: Date
    old_context: Context
    new_context: Context
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a transfer initialized from the given database row'''
        id = row['id']
        context = row.context()
        bus = Bus.find(context, row['bus_number'])
        old_context = row.context(system_key='old_system_id')
        new_context = row.context(system_key='new_system_id')
        date = Date.parse(row['date'], new_context.timezone)
        return cls(id, bus, date, old_context, new_context)
