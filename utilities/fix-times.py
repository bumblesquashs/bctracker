#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database
import helpers.model
import helpers.order
import helpers.system
from models.date import Date
from models.record import Record
from models.time import Time

helpers.model.default.load()
helpers.order.default.load()
helpers.system.default.load()

database.default.connect(foreign_keys=False)

rows = database.default.select('record', 
    columns={
        'record.record_id': 'record_id',
        'record.bus_number': 'record_bus_number',
        'record.date': 'record_date',
        'record.system_id': 'record_system_id',
        'record.block_id': 'record_block_id',
        'record.routes': 'record_routes',
        'record.start_time': 'record_start_time',
        'record.end_time': 'record_end_time',
        'record.first_seen': 'record_first_seen',
        'record.last_seen': 'record_last_seen'
    },
    filters=[
        "(record.start_time is not null AND record.start_time < '04:00')",
        "(record.end_time is not null AND record.end_time < '04:00')",
        "(record.first_seen is not null AND record.first_seen < '04:00')",
        "(record.last_seen is not null AND record.last_seen < '04:00')",
        "record.system_id = 'creston-valley'"
    ],
    operation='OR')
records = [Record.from_db(row) for row in rows]

base_time = Time(4, 0, 0, False, None)
start_date = Date(2022, 11, 6, None)
end_date = Date(2023, 3, 12, None)
for record in records:
    if record.start_time < base_time:
        time = record.start_time
        record.start_time = Time(time.hour + 24, time.minute, time.second, time.accurate_seconds, time.timezone)
    if record.end_time < base_time:
        time = record.end_time
        record.end_time = Time(time.hour + 24, time.minute, time.second, time.accurate_seconds, time.timezone)
    if record.first_seen < base_time:
        time = record.first_seen
        record.first_seen = Time(time.hour + 24, time.minute, time.second, time.accurate_seconds, time.timezone)
    if record.last_seen < base_time:
        time = record.last_seen
        record.last_seen = Time(time.hour + 24, time.minute, time.second, time.accurate_seconds, time.timezone)
    if record.system.id == 'creston-valley' and record.date >= start_date and record.date < end_date:
        print(f'UPDATING {record.date}')
        time = record.first_seen
        record.first_seen = Time(time.hour + 1, time.minute, time.second, time.accurate_seconds, time.timezone)
        time = record.last_seen
        record.last_seen = Time(time.hour + 1, time.minute, time.second, time.accurate_seconds, time.timezone)
    database.default.update('record',
        values={
            'start_time': record.start_time.format_db(),
            'end_time': record.end_time.format_db(),
            'first_seen': record.first_seen.format_db(),
            'last_seen': record.last_seen.format_db()
        },
        filters={
            'record_id': record.id
        })

database.default.commit()
database.default.disconnect()
