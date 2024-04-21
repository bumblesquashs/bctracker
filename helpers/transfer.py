
from models.transfer import Transfer

import database

class TransferService:
    
    def create(self, bus, date, old_system, new_system):
        '''Inserts a new transfer into the database'''
        bus_number = getattr(bus, 'number', bus)
        old_system_id = getattr(old_system, 'id', old_system)
        new_system_id = getattr(new_system, 'id', new_system)
        database.insert('transfer', {
            'bus_number': bus_number,
            'date': date.format_db(),
            'old_system_id': old_system_id,
            'new_system_id': new_system_id
        })
    
    def find_all(self, old_system=None, new_system=None, bus=None, limit=None):
        '''Returns all transfers that match the given system'''
        old_system_id = getattr(old_system, 'id', old_system)
        new_system_id = getattr(new_system, 'id', new_system)
        bus_number = getattr(bus, 'number', bus)
        return database.select('transfer',
            columns={
                'transfer.transfer_id': 'transfer_id',
                'transfer.bus_number': 'transfer_bus_number',
                'transfer.date': 'transfer_date',
                'transfer.old_system_id': 'transfer_old_system_id',
                'transfer.new_system_id': 'transfer_new_system_id'
            },
            filters={
                'transfer.old_system_id': old_system_id,
                'transfer.new_system_id': new_system_id,
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

default = TransferService()
