
from models.transfer import Transfer

import database

def create(bus, date, old_system, new_system):
    database.insert('transfers', {
        'bus_number': bus.number,
        'date': date.format_db(),
        'old_system_id': old_system.id,
        'new_system_id': new_system.id
    })

def find_all(system_id, limit=None):
    rows = database.select('transfers',
        columns={
            'transfers.transfer_id': 'transfer_id',
            'transfers.bus_number': 'transfer_bus_number',
            'transfers.date': 'transfer_date',
            'transfers.old_system_id': 'transfer_old_system_id',
            'transfers.new_system_id': 'transfer_new_system_id'
        },
        filters={
            'transfers.old_system_id': system_id,
            'transfers.new_system_id': system_id
        },
        operation='OR',
        order_by={
            'transfers.date': 'DESC',
            'transfers.transfer_id': 'DESC'
        },
        limit=limit)
    return [Transfer.from_db(row) for row in rows]
