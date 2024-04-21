#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database
from models.record import Record
import helpers.system

helpers.system.default.load()

database = Database()
database.connect(foreign_keys=False)

database.execute('''
    INSERT INTO record (record_id, bus_number, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen)
    SELECT record_id, bus_number, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen
    FROM records
''')
database.execute('''
    INSERT INTO trip_record (trip_record_id, record_id, trip_id)
    SELECT trip_record_id, record_id, trip_id
    FROM trip_records
''')
database.execute('''
    INSERT INTO transfer (transfer_id, bus_number, date, old_system_id, new_system_id)
    SELECT transfer_id, bus_number, date, old_system_id, new_system_id
    FROM transfers
''')

database.execute('DROP TABLE records')
database.execute('DROP TABLE trip_records')
database.execute('DROP TABLE transfers')

def find_numbered(row_number_column):
    cte, args = database.build_select('record',
        columns={
            'record.record_id': 'record_id',
            'record.bus_number': 'bus_number',
            'record.date': 'date',
            'record.system_id': 'system_id',
            'record.block_id': 'block_id',
            'record.routes': 'routes',
            'record.start_time': 'start_time',
            'record.end_time': 'end_time',
            'record.first_seen': 'first_seen',
            'record.last_seen': 'last_seen',
            row_number_column: 'row_number'
        })
    rows = database.select('numbered_record',
        columns={
            'numbered_record.record_id': 'record_id',
            'numbered_record.bus_number': 'record_bus_number',
            'numbered_record.date': 'record_date',
            'numbered_record.system_id': 'record_system_id',
            'numbered_record.block_id': 'record_block_id',
            'numbered_record.routes': 'record_routes',
            'numbered_record.start_time': 'record_start_time',
            'numbered_record.end_time': 'record_end_time',
            'numbered_record.first_seen': 'record_first_seen',
            'numbered_record.last_seen': 'record_last_seen'
        },
        ctes={
            'numbered_record': cte
        },
        filters={
            'numbered_record.row_number': 1
        },
        custom_args=args)
    return [Record.from_db(row) for row in rows]

first_records = find_numbered('ROW_NUMBER() OVER(PARTITION BY record.bus_number ORDER BY record.date ASC, record.record_id ASC)')
last_records = find_numbered('ROW_NUMBER() OVER(PARTITION BY record.bus_number ORDER BY record.date DESC, record.record_id DESC)')

first_records = {r.bus: r for r in first_records}
last_records = {r.bus: r for r in last_records}

for bus in first_records.keys():
    first_record = first_records[bus]
    last_record = last_records[bus]
    database.insert('overview', {
        'bus_number': bus.number,
        'first_seen_date': first_record.date.format_db(),
        'first_seen_system_id': first_record.system.id,
        'first_record_id': first_record.id,
        'last_seen_date': last_record.date.format_db(),
        'last_seen_system_id': last_record.system.id,
        'last_record_id': last_record.id
    })

database.commit()
database.disconnect()
