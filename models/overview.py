
from models.bus import Bus
from models.context import Context
from models.date import Date
from models.record import Record

class Overview:
    '''An overview of a bus' history'''
    
    __slots__ = (
        'bus',
        'first_seen_date',
        'first_seen_context',
        'first_record',
        'last_seen_date',
        'last_seen_context',
        'last_record'
    )
    
    @classmethod
    def from_db(cls, row, prefix='overview'):
        '''Returns an overview initialized from the given database row'''
        context = Context.find(agency_id='bc-transit')
        bus = Bus.find(context, row[f'{prefix}_bus_number'])
        first_seen_context = Context.find(system_id=row[f'{prefix}_first_seen_system_id'])
        first_seen_date = Date.parse(row[f'{prefix}_first_seen_date'], first_seen_context.timezone)
        if row[f'{prefix}_first_record_id'] is None:
            first_record = None
        else:
            first_record = Record.from_db(row, prefix=f'{prefix}_first_record')
        last_seen_context = Context.find(system_id=row[f'{prefix}_last_seen_system_id'])
        last_seen_date = Date.parse(row[f'{prefix}_last_seen_date'], last_seen_context.timezone)
        if row[f'{prefix}_last_record_id'] is None:
            last_record = None
        else:
            last_record = Record.from_db(row, prefix=f'{prefix}_last_record')
        return cls(bus, first_seen_date, first_seen_context, first_record, last_seen_date, last_seen_context, last_record)
    
    def __init__(self, bus, first_seen_date, first_seen_context: Context, first_record, last_seen_date, last_seen_context: Context, last_record):
        self.bus = bus
        self.first_seen_date = first_seen_date
        self.first_seen_context = first_seen_context
        self.first_record = first_record
        self.last_seen_date = last_seen_date
        self.last_seen_context = last_seen_context
        self.last_record = last_record
