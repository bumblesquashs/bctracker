
from models.transfer import Transfer

import database

def create(bus, date, old_system, new_system):
    '''Inserts a new transfer into the database'''
    database.insert('transfer', {
        'bus_number': bus.number,
        'date': date.format_db(),
        'old_system_id': old_system.id,
        'new_system_id': new_system.id
    })

def find_all(system_id, limit=None):
    '''Returns all transfers that match the given system ID'''
    return database.select('transfer',
        columns={
            'transfer.transfer_id': 'transfer_id',
            'transfer.bus_number': 'transfer_bus_number',
            'transfer.date': 'transfer_date',
            'transfer.old_system_id': 'transfer_old_system_id',
            'transfer.new_system_id': 'transfer_new_system_id'
        },
        filters={
            'transfer.old_system_id': system_id,
            'transfer.new_system_id': system_id
        },
        operation='OR',
        order_by={
            'transfer.date': 'DESC',
            'transfer.transfer_id': 'DESC'
        },
        limit=limit,
        initializer=Transfer.from_db)
