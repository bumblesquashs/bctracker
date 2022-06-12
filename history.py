
from datetime import datetime, timedelta

from models.bus import Bus
from models.record import Record
from models.time import Time
from models.transfer import Transfer

import database
import formatting

def update(positions):
    for position in positions:
        system = position.system
        bus = position.bus
        trip = position.trip
        if bus.number < 0 or trip is None:
            continue
        block = trip.block
        hour = datetime.now().hour
        today = datetime.today()
        date = today if hour >= 4 else today - timedelta(days=1)
        now = Time.now()
        
        records = get_records(bus_number=bus.number, limit=1)
        if len(records) > 0:
            last_record = records[0]
            if last_record.system_id != system.id:
                database.insert('transfers', {
                    'bus_number': bus.number,
                    'date': formatting.database(date),
                    'old_system_id': last_record.system_id,
                    'new_system_id': system.id
                })
            if last_record.date.date() == date.date() and last_record.block_id == block.id:
                database.update('records',
                    values={
                        'last_seen': str(now)
                    },
                    filters={
                        'record_id': last_record.id
                    })
                trip_ids = get_trip_ids(last_record)
                if trip.id not in trip_ids:
                    database.insert('trip_records', {
                        'record_id': last_record.id,
                        'trip_id': trip.id
                    })
                continue
        
        record_id = database.insert('records', {
            'bus_number': bus.number,
            'date': formatting.database(date),
            'system_id': system.id,
            'block_id': block.id,
            'routes': block.get_routes_string(),
            'start_time': block.get_start_time().full_string,
            'end_time': block.get_end_time().full_string,
            'first_seen': now.full_string,
            'last_seen': now.full_string
        })
        database.insert('trip_records', {
            'record_id': record_id,
            'trip_id': trip.id
        })
    database.commit()

def get_last_seen(system_id):
    row_number_column = 'ROW_NUMBER() OVER(PARTITION BY records.bus_number ORDER BY records.date DESC, records.record_id DESC)'
    order_by = 'numbered_records.bus_number'
    return get_numbered_records(system_id, row_number_column, order_by)

def get_first_seen(system_id):
    row_number_column = 'ROW_NUMBER() OVER(PARTITION BY records.bus_number ORDER BY records.date ASC, records.record_id ASC)'
    order_by = {
        'numbered_records.date': 'DESC',
        'numbered_records.record_id': 'DESC'
    }
    return get_numbered_records(system_id, row_number_column, order_by)

def get_numbered_records(system_id, row_number_column, order_by):
    cte, args = database.build_select('records',
        columns={
            'records.record_id': 'record_id',
            'records.bus_number': 'bus_number',
            'records.date': 'date',
            'records.system_id': 'system_id',
            'records.block_id': 'block_id',
            'records.routes': 'routes',
            'records.start_time': 'start_time',
            'records.end_time': 'end_time',
            'records.first_seen': 'first_seen',
            'records.last_seen': 'last_seen',
            row_number_column: 'row_number'
        })
    rows = database.select('numbered_records',
        columns={
            'numbered_records.record_id': 'record_id',
            'numbered_records.bus_number': 'record_bus_number',
            'numbered_records.date': 'record_date',
            'numbered_records.system_id': 'record_system_id',
            'numbered_records.block_id': 'record_block_id',
            'numbered_records.routes': 'record_routes',
            'numbered_records.start_time': 'record_start_time',
            'numbered_records.end_time': 'record_end_time',
            'numbered_records.first_seen': 'record_first_seen',
            'numbered_records.last_seen': 'record_last_seen'
        },
        ctes={
            'numbered_records': cte
        },
        filters={
            'numbered_records.row_number': 1,
            'numbered_records.system_id': system_id
        },
        order_by=order_by,
        custom_args=args)
    return [Record(row) for row in rows]

def get_records(system_id=None, bus_number=None, block_id=None, limit=None):
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
        filters={
            'records.system_id': system_id,
            'records.bus_number': bus_number,
            'records.block_id': block_id
        },
        order_by={
            'records.date': 'DESC',
            'records.record_id': 'DESC'
        },
        limit=limit)
    return [Record(row) for row in rows]

def get_trip_ids(record):
    rows = database.select('trip_records', columns=['trip_id'], filters={'record_id': record.id})
    return {row['trip_id'] for row in rows}

def get_trip_records(trip, limit=None):
    rows = database.select('trip_records',
        columns={
            'trip_records.record_id': 'record_id',
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
        joins={
            'records': {
                'records.record_id': 'trip_records.record_id'
            }
        },
        filters={
            'trip_records.trip_id': trip.id,
            'records.system_id': trip.system.id
        },
        order_by={
            'records.date': 'DESC',
            'trip_records.record_id': 'DESC'
        },
        limit=limit)
    return [Record(row) for row in rows]

def get_transfers(system_id, limit=None):
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
    return [Transfer(row) for row in rows]

def recorded_buses(system_id):
    rows = database.select('records',
        columns={
            'records.bus_number': 'bus_number'
        },
        distinct=True,
        filters={
            'records.system_id': system_id
        })
    return [row['bus_number'] for row in rows]

def recorded_today(system_id, trips):
    hour = datetime.now().hour
    today = datetime.today()
    date = today if hour >= 4 else today - timedelta(days=1)
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
            'records.date': formatting.database(date),
            'trip_records.trip_id': [t.id for t in trips]
        })
    return {row['trip_id']: Bus(row['bus_number']) for row in rows}

def scheduled_today(system_id, trips):
    hour = datetime.now().hour
    today = datetime.today()
    date = today if hour >= 4 else today - timedelta(days=1)
    cte, args = database.build_select('records',
        columns={
            'records.bus_number': 'bus_number',
            'records.block_id': 'block_id',
            'ROW_NUMBER() OVER(PARTITION BY records.block_id ORDER BY records.record_id DESC)': 'row_number'
        },
        filters={
            'records.system_id': system_id,
            'records.date': formatting.database(date),
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
