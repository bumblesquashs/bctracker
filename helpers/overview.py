
from models.overview import Overview

import database

def create(system, agency, bus, date, record):
    '''Inserts a new overview into the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    bus_number = getattr(bus, 'number', bus)
    record_id = getattr(record, 'id', record)
    database.insert('overview', {
        'agency_id': agency_id,
        'bus_number': bus_number,
        'first_seen_date': date.format_db(),
        'first_seen_system_id': system_id,
        'first_record_id': record_id,
        'last_seen_date': date.format_db(),
        'last_seen_system_id': system_id,
        'last_record_id': record_id
    })

def find(agency, bus):
    '''Returns the overview of the given bus'''
    overviews = find_all(agency=agency, bus=bus, limit=1)
    if len(overviews) == 1:
        return overviews[0]
    return None

def find_all(system=None, last_seen_system=None, agency=None, bus=None, limit=None):
    '''Returns all overviews that match the given system and bus'''
    system_id = getattr(system, 'id', system)
    last_seen_system_id = getattr(last_seen_system, 'id', last_seen_system)
    agency_id = getattr(agency, 'id', agency)
    bus_number = getattr(bus, 'number', bus)
    return database.select('overview',
        columns={
            'overview.agency_id': 'overview_agency_id',
            'overview.bus_number': 'overview_bus_number',
            'overview.first_seen_date': 'overview_first_seen_date',
            'overview.first_seen_system_id': 'overview_first_seen_system_id',
            'overview.last_seen_date': 'overview_last_seen_date',
            'overview.last_seen_system_id': 'overview_last_seen_system_id',
            'first_record.record_id': 'overview_first_record_id',
            'first_record.agency_id': 'overview_first_record_agency_ic',
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
            'last_record.agency_id': 'overview_last_record_agency_id',
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
            'overview.agency_id': agency_id,
            'overview.bus_number': bus_number,
            'last_record.system_id': system_id,
            'overview.last_seen_system_id': last_seen_system_id
        },
        limit=limit,
        initializer=Overview.from_db
    )

def find_bus_numbers(system=None, agency=None):
    '''Returns all bus numbers that have been seen'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    joins = {}
    filters = {
        'overview.agency_id': agency_id
    }
    if system_id is not None:
        joins['record last_record'] = {
            'last_record.record_id': 'overview.last_record_id'
        }
        filters['last_record.system_id'] = system_id
    return database.select('overview',
        columns={
            'overview.bus_number': 'bus_number'
        },
        join_type='LEFT',
        joins=joins,
        filters=filters,
        initializer=lambda r: r['bus_number']
    )

def update(overview, date, system, record):
    '''Updates an overview in the database'''
    system_id = getattr(system, 'id', system)
    record_id = getattr(record, 'id', record)
    values = {
        'last_seen_date': date.format_db(),
        'last_seen_system_id': system_id
    }
    if record_id is not None:
        if overview.first_record is None:
            values['first_record_id'] = record_id
        values['last_record_id'] = record_id
    database.update('overview', values, {
        'agency_id': overview.agency.id,
        'bus_number': overview.bus.number
    })
