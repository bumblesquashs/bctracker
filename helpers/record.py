
from models.bus import Bus
from models.date import Date
from models.record import Record

import database

def create(system, agency, bus, date, block, time, trip):
    '''Inserts a new record into the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    bus_number = getattr(bus, 'number', bus)
    block_id = getattr(block, 'id', block)
    record_id = database.insert('record', {
        'system_id': system_id,
        'agency_id': agency_id,
        'bus_number': bus_number,
        'date': date.format_db(),
        'block_id': block_id,
        'routes': block.get_routes_string(date=date),
        'start_time': block.get_start_time(date=date).format_db(),
        'end_time': block.get_end_time(date=date).format_db(),
        'first_seen': time.format_db(),
        'last_seen': time.format_db()
    })
    create_trip(record_id, trip)
    return record_id

def create_trip(record, trip):
    '''Inserts a new trip record into the database'''
    record_id = getattr(record, 'id', record)
    trip_id = getattr(trip, 'id', trip)
    database.insert('trip_record', {
        'record_id': record_id,
        'trip_id': trip_id
    })

def update(record, time):
    '''Updates a record in the database'''
    record_id = getattr(record, 'id', record)
    database.update('record',
        values={
            'last_seen': time.format_db()
        },
        filters={
            'record_id': record_id
        }
    )

def find_all(system=None, agency=None, bus=None, block=None, trip=None, limit=None):
    '''Returns all records that match the given system, bus, block, and trip'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    bus_number = getattr(bus, 'number', bus)
    block_id = getattr(block, 'id', block)
    trip_id = getattr(trip, 'id', trip)
    joins = {}
    filters = {
        'record.system_id': system_id,
        'record.agency_id': agency_id,
        'record.bus_number': bus_number,
        'record.block_id': block_id
    }
    if trip_id is not None:
        joins['trip_record'] = {
            'trip_record.record_id': 'record.record_id'
        }
        filters['trip_record.trip_id'] = trip_id
    return database.select('record', 
        columns={
            'record.record_id': 'record_id',
            'record.system_id': 'record_system_id',
            'record.agency_id': 'record_agency_id',
            'record.bus_number': 'record_bus_number',
            'record.date': 'record_date',
            'record.block_id': 'record_block_id',
            'record.routes': 'record_routes',
            'record.start_time': 'record_start_time',
            'record.end_time': 'record_end_time',
            'record.first_seen': 'record_first_seen',
            'record.last_seen': 'record_last_seen'
        },
        joins=joins,
        filters=filters,
        order_by={
            'record.date': 'DESC',
            'record.record_id': 'DESC'
        },
        limit=limit,
        initializer=Record.from_db
    )

def find_trip_ids(record):
    '''Returns all trip IDs associated with the given record'''
    record_id = getattr(record, 'id', record)
    return database.select('trip_record', columns=['trip_id'], filters={'record_id': record_id}, initializer=lambda r: r['trip_id'])

def find_recorded_today(system, agency, trips):
    '''Returns all bus numbers matching the given system and trips that were recorded on the current date'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    trip_ids = [getattr(t, 'id', t) for t in trips]
    date = Date.today(system.timezone)
    rows = database.select('trip_record',
        columns={
            'trip_record.trip_id': 'trip_id',
            'record.bus_number': 'bus_number'
        },
        joins={
            'record': {
                'record.record_id': 'trip_record.record_id'
            }
        },
        filters={
            'record.system_id': system_id,
            'record.agency_id': agency_id,
            'record.date': date.format_db(),
            'trip_record.trip_id': trip_ids
        },
        order_by='record.last_seen ASC'
    )
    return {row['trip_id']: Bus.find(agency, row['bus_number']) for row in rows}

def find_scheduled_today(system, agency, trips):
    '''Returns all bus numbers matching the given system and trips that are scheduled to run on the current date'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    block_ids = list({t.block_id for t in trips})
    date = Date.today(system.timezone)
    cte, args = database.build_select('record',
        columns={
            'record.bus_number': 'bus_number',
            'record.block_id': 'block_id',
            'record.last_seen': 'last_seen',
            'ROW_NUMBER() OVER(PARTITION BY record.block_id ORDER BY record.record_id DESC)': 'row_number'
        },
        filters={
            'record.system_id': system_id,
            'record.agency_id': agency_id,
            'record.date': date.format_db(),
            'record.block_id': block_ids
        }
    )
    rows = database.select('numbered_record',
        columns={
            'numbered_record.block_id': 'block_id',
            'numbered_record.bus_number': 'bus_number'
        },
        ctes={
            'numbered_record': cte
        },
        filters={
            'numbered_record.row_number': 1
        },
        order_by='numbered_record.last_seen ASC',
        custom_args=args
    )
    return {row['block_id']: Bus.find(agency, row['bus_number']) for row in rows}
