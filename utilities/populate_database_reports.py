#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database
from models.record import Record
import helpers.system

helpers.system.load()

database.connect()

def find_numbered(row_number_column):
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
            'numbered_records.row_number': 1
        },
        custom_args=args)
    return [Record.from_db(row) for row in rows]

first_records = find_numbered('ROW_NUMBER() OVER(PARTITION BY records.bus_number ORDER BY records.date ASC, records.record_id ASC)')
last_records = find_numbered('ROW_NUMBER() OVER(PARTITION BY records.bus_number ORDER BY records.date DESC, records.record_id DESC)')

first_records = {r.bus: r for r in first_records}
last_records = {r.bus: r for r in last_records}

for bus in first_records.keys():
    first_record = first_records[bus]
    last_record = last_records[bus]
    database.insert('reports', {
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
