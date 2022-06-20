
from models.bus import Bus
from models.date import Date
from models.record import Record

import database

def create(bus, date, system, block, time, trip):
    record_id = database.insert('records', {
        'bus_number': bus.number,
        'date': date.format_db(),
        'system_id': system.id,
        'block_id': block.id,
        'routes': block.get_routes_string(),
        'start_time': block.get_start_time().format_db(),
        'end_time': block.get_end_time().format_db(),
        'first_seen': time.format_db(),
        'last_seen': time.format_db()
    })
    create_trip(record_id, trip)
    return record_id

def create_trip(record_id, trip):
    database.insert('trip_records', {
        'record_id': record_id,
        'trip_id': trip.id
    })

def update(record_id, time):
    database.update('records',
        values={
            'last_seen': time.format_db()
        },
        filters={
            'record_id': record_id
        })

def find_all(system_id=None, bus_number=None, block_id=None, trip_id=None, limit=None):
    joins = {}
    filters = {
        'records.system_id': system_id,
        'records.bus_number': bus_number,
        'records.block_id': block_id
    }
    if trip_id is not None:
        joins['trip_records'] = {
            'trip_records.record_id': 'records.record_id'
        }
        filters['trip_records.trip_id'] = trip_id
    rows = database.select('records', 
        columns={
            'records.record_id': 'record_id',
            'records.bus_number': 'record_bus_number',
            'records.date': 'record_date',
            'records.system_id': 'record_system_id',
            'records.block_id': 'record_block_id',
            'records.routes': 'record_routes',
            'records.start_time': 'record_start_time',
            'records.end_time': 'record_end_time',
            'records.first_seen': 'record_first_seen',
            'records.last_seen': 'record_last_seen'
        },
        joins=joins,
        filters=filters,
        order_by={
            'records.date': 'DESC',
            'records.record_id': 'DESC'
        },
        limit=limit)
    return [Record.from_db(row) for row in rows]

def find_trip_ids(record):
    rows = database.select('trip_records', columns=['trip_id'], filters={'record_id': record.id})
    return {row['trip_id'] for row in rows}

def find_recorded_buses(system_id):
    rows = database.select('records',
        columns={
            'records.bus_number': 'bus_number'
        },
        distinct=True,
        filters={
            'records.system_id': system_id
        })
    return [row['bus_number'] for row in rows]

def find_recorded_today(system_id, trips):
    today = Date.today()
    rows = database.select('trip_records',
        columns={
            'trip_records.trip_id': 'trip_id',
            'records.bus_number': 'bus_number'
        },
        joins={
            'records': {
                'records.record_id': 'trip_records.record_id'
            }
        },
        filters={
            'records.system_id': system_id,
            'records.date': today.format_db(),
            'trip_records.trip_id': [t.id for t in trips]
        })
    return {row['trip_id']: Bus(row['bus_number']) for row in rows}

def find_scheduled_today(system_id, trips):
    today = Date.today()
    cte, args = database.build_select('records',
        columns={
            'records.bus_number': 'bus_number',
            'records.block_id': 'block_id',
            'ROW_NUMBER() OVER(PARTITION BY records.block_id ORDER BY records.record_id DESC)': 'row_number'
        },
        filters={
            'records.system_id': system_id,
            'records.date': today.format_db(),
            'records.block_id': list({t.block_id for t in trips})
        })
    rows = database.select('numbered_records',
        columns={
            'numbered_records.block_id': 'block_id',
            'numbered_records.bus_number': 'bus_number'
        },
        ctes={
            'numbered_records': cte
        },
        filters={
            'numbered_records.row_number': 1
        },
        custom_args=args)
    return {row['block_id']: Bus(row['bus_number']) for row in rows}
