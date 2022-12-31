
from models.overview import Overview

import database

def create(bus, date, system, record_id):
    '''Inserts a new overview into the database'''
    database.insert('overview', {
        'bus_number': bus.number,
        'first_seen_date': date.format_db(),
        'first_seen_system_id': system.id,
        'first_record_id': record_id,
        'last_seen_date': date.format_db(),
        'last_seen_system_id': system.id,
        'last_record_id': record_id
    })

def find(bus_number):
    '''Returns the overview of the given bus number'''
    overviews = find_all(bus_number=bus_number, limit=1)
    if len(overviews) == 1:
        return overviews[0]
    return None

def find_all(system_id=None, bus_number=None, limit=None):
    '''Returns all overviews that match the given system ID and bus number'''
    rows = database.select('overview',
        columns={
            'overview.bus_number': 'overview_bus_number',
            'overview.first_seen_date': 'overview_first_seen_date',
            'overview.first_seen_system_id': 'overview_first_seen_system_id',
            'overview.last_seen_date': 'overview_last_seen_date',
            'overview.last_seen_system_id': 'overview_last_seen_system_id',
            'first_record.record_id': 'overview_first_record_id',
            'first_record.bus_number': 'overview_first_record_bus_number',
            'first_record.date': 'overview_first_record_date',
            'first_record.system_id': 'overview_first_record_system_id',
            'first_record.block_id': 'overview_first_record_block_id',
            'first_record.routes': 'overview_first_record_routes',
            'first_record.start_time': 'overview_first_record_start_time',
            'first_record.end_time': 'overview_first_record_end_time',
            'first_record.first_seen': 'overview_first_record_first_seen',
            'first_record.last_seen': 'overview_first_record_last_seen',
            'last_record.record_id': 'overview_last_record_id',
            'last_record.bus_number': 'overview_last_record_bus_number',
            'last_record.date': 'overview_last_record_date',
            'last_record.system_id': 'overview_last_record_system_id',
            'last_record.block_id': 'overview_last_record_block_id',
            'last_record.routes': 'overview_last_record_routes',
            'last_record.start_time': 'overview_last_record_start_time',
            'last_record.end_time': 'overview_last_record_end_time',
            'last_record.first_seen': 'overview_last_record_first_seen',
            'last_record.last_seen': 'overview_last_record_last_seen'
        },
        join_type='LEFT',
        joins={
            'record first_record': {
                'first_record.record_id': 'overview.first_record_id'
            },
            'record last_record': {
                'last_record.record_id': 'overview.last_record_id'
            }
        },
        filters={
            'overview.bus_number': bus_number,
            'last_record.system_id': system_id
        },
        limit=limit)
    return [Overview.from_db(row) for row in rows]

def find_bus_numbers(system_id=None):
    joins = {}
    filters = {}
    if system_id is not None:
        joins['record last_record'] = {
            'last_record.record_id': 'overview.last_record_id'
        }
        filters['last_record.system_id'] = system_id
    rows = database.select('overview',
        columns={
            'overview.bus_number': 'bus_number'
        },
        join_type='LEFT',
        joins=joins,
        filters=filters
    )
    return [row['bus_number'] for row in rows]

def update(overview, date, system, record_id):
    '''Updates an overview in the database'''
    values = {
        'last_seen_date': date.format_db(),
        'last_seen_system_id': system.id
    }
    if record_id is not None:
        if overview.first_record is None:
            values['first_record_id'] = record_id
        values['last_record_id'] = record_id
    database.update('overview', values, {
        'bus_number': overview.bus.number
    })
