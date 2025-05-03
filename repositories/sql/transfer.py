
from database import Database

from models.context import Context
from models.transfer import Transfer

from repositories import TransferRepository

class SQLTransferRepository(TransferRepository):
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database: Database):
        self.database = database
    
    def create(self, bus, date, old_context: Context, new_context: Context, ):
        '''Inserts a new transfer into the database'''
        bus_number = getattr(bus, 'number', bus)
        self.database.insert('transfer', {
            'bus_number': bus_number,
            'date': date.format_db(),
            'old_system_id': old_context.system_id,
            'new_system_id': new_context.system_id
        })
    
    def find_all(self, old_context: Context, new_context: Context, bus=None, limit=None):
        '''Returns all transfers that match the given system'''
        bus_number = getattr(bus, 'number', bus)
        return self.database.select('transfer',
            columns={
                'transfer.transfer_id': 'transfer_id',
                'transfer.bus_number': 'transfer_bus_number',
                'transfer.date': 'transfer_date',
                'transfer.old_system_id': 'transfer_old_system_id',
                'transfer.new_system_id': 'transfer_new_system_id'
            },
            filters={
                'transfer.old_system_id': old_context.system_id,
                'transfer.new_system_id': new_context.system_id,
                'transfer.bus_number': bus_number
            },
            operation='OR',
            order_by={
                'transfer.date': 'DESC',
                'transfer.transfer_id': 'DESC'
            },
            limit=limit,
            initializer=Transfer.from_db
        )
