#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

restore_date = '2023-11-14'

db1 = Database()
db2 = Database(name='restore')

db1.connect()
db2.connect()

overview_rows = db1.select('overview',
    columns={
        'overview.bus_number': 'bus_number',
        'overview.first_seen_date': 'first_seen_date',
        'overview.first_seen_system_id': 'first_seen_system_id',
        'overview.last_seen_date': 'last_seen_date',
        'overview.last_seen_system_id': 'last_seen_system_id'
    },
    filters={
        'overview.first_seen_date': {
            '>=': restore_date
        },
        'overview.last_seen_date': {
            '>=': restore_date
        }
    },
    operation='OR')

print(f'Updating {len(overview_rows)} overviews')

for i, row in enumerate(overview_rows):
    print(f'  Updating overview {i}')
    if row['first_seen_date'] >= restore_date:
        db2.insert('overview', {
            'bus_number': row['bus_number'],
            'first_seen_date': row['first_seen_date'],
            'first_seen_system_id': row['first_seen_system_id'],
            'last_seen_date': row['last_seen_date'],
            'last_seen_system_id': row['last_seen_system_id']
        })
    else:
        db2.update('overview',
            values={
                'last_seen_date': row['last_seen_date'],
                'last_seen_system_id': row['last_seen_system_id']
            },
            filters={
                'bus_number': row['bus_number']
            })

record_rows = db1.select('record', 
    columns={
        'record.record_id': 'id',
        'record.bus_number': 'bus_number',
        'record.date': 'date',
        'record.system_id': 'system_id',
        'record.block_id': 'block_id',
        'record.routes': 'routes',
        'record.start_time': 'start_time',
        'record.end_time': 'end_time',
        'record.first_seen': 'first_seen',
        'record.last_seen': 'last_seen'
    },
    filters={
        'record.date': {
            '>=': restore_date
        }
    })

print(f'Moving {len(record_rows)} records')

for i, row in enumerate(record_rows):
    print(f'  Moving record {i}')
    trip_record_rows = db1.select('trip_record',
        columns={
            'trip_record.trip_id': 'trip_id'
        },
        joins={
            'record': {
                'record.record_id': 'trip_record.record_id'
            }
        },
        filters={
            'record.record_id': row['id']
        })
    first_overview_rows = db1.select('overview',
        columns={
            'overview.bus_number': 'bus_number'
        },
        filters={
            'overview.first_record_id': row['id']
        })
    last_overview_rows = db1.select('overview',
        columns={
            'overview.bus_number': 'bus_number'
        },
        filters={
            'overview.last_record_id': row['id']
        })
    
    new_id = db2.insert('record', {
        'bus_number': row['bus_number'],
        'date': row['date'],
        'system_id': row['system_id'],
        'block_id': row['block_id'],
        'routes': row['routes'],
        'start_time': row['start_time'],
        'end_time': row['end_time'],
        'first_seen': row['first_seen'],
        'last_seen': row['last_seen']
    })
    print(f'  Moving {len(trip_record_rows)} trip records')
    print(f'  Updating {len(first_overview_rows)} overview first records')
    print(f'  Updating {len(trip_record_rows)} overview last records')
    for trip_row in trip_record_rows:
        db2.insert('trip_record', {
            'record_id': new_id,
            'trip_id': trip_row['trip_id']
        })
    for overview_row in first_overview_rows:
        db2.update('overview',
            values={
                'first_record_id': new_id
            },
            filters={
                'overview.bus_number': overview_row['bus_number']
            })
    for overview_row in last_overview_rows:
        db2.update('overview',
            values={
                'last_record_id': new_id
            },
            filters={
                'overview.bus_number': overview_row['bus_number']
            })

transfer_rows = db1.select('transfer',
    columns={
        'transfer.bus_number': 'bus_number',
        'transfer.date': 'date',
        'transfer.old_system_id': 'old_system_id',
        'transfer.new_system_id': 'new_system_id'
    },
    filters={
        'transfer.date': {
            '>=': restore_date
        }
    })

print(f'Moving {len(transfer_rows)} transfers')

for i, row in enumerate(transfer_rows):
    print(f'  Moving transfer {i}')
    db2.insert('transfer', row)

db1.commit()
db2.commit()

db1.disconnect()
db2.disconnect()
