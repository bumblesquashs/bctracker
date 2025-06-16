
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.transfer import Transfer

@dataclass(slots=True)
class TransferRepository:
    
    database: Database
    
    def create(self, bus, date, old_context: Context, new_context: Context):
        '''Inserts a new transfer into the database'''
        bus_number = getattr(bus, 'number', bus)
        self.database.insert('transfer', {
            'bus_number': bus_number,
            'date': date.format_db(),
            'old_system_id': old_context.system_id,
            'new_system_id': new_context.system_id
        })
    
    def find_all(self, old_context: Context = Context(), new_context: Context = Context(), bus=None, limit=None) -> list[Transfer]:
        '''Returns all transfers that match the given system'''
        bus_number = getattr(bus, 'number', bus)
        return self.database.select('transfer',
            columns={
                'transfer.transfer_id': 'id',
                'transfer.bus_number': 'bus_number',
                'transfer.date': 'date',
                'transfer.old_system_id': 'old_system_id',
                'transfer.new_system_id': 'new_system_id'
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
