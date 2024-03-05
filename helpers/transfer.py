
from models.transfer import Transfer

import database

def create(agency, bus, date, old_system, new_system):
    '''Inserts a new transfer into the database'''
    agency_id = getattr(agency, 'id', agency)
    bus_number = getattr(bus, 'number', bus)
    old_system_id = getattr(old_system, 'id', old_system)
    new_system_id = getattr(new_system, 'id', new_system)
    database.insert('transfer', {
        'agency_id': agency_id,
        'bus_number': bus_number,
        'date': date.format_db(),
        'old_system_id': old_system_id,
        'new_system_id': new_system_id
    })

def find_all(system=None, agency=None, bus=None, limit=None):
    '''Returns all transfers'''
    agency_id = getattr(agency, 'id', agency)
    system_id = getattr(system, 'id', system)
    bus_number = getattr(bus, 'number', bus)
    return database.select('transfer',
        columns={
            'transfer.transfer_id': 'transfer_id',
            'transfer.agency_id': 'transfer_agency_id',
            'transfer.bus_number': 'transfer_bus_number',
            'transfer.date': 'transfer_date',
            'transfer.old_system_id': 'transfer_old_system_id',
            'transfer.new_system_id': 'transfer_new_system_id'
        },
        filters={
            'transfer.agency_id': agency_id,
            'transfer.old_system_id': system_id,
            'transfer.new_system_id': system_id,
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
