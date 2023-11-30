#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

restore_date = '2023-11-14'

database.connect('bctracker')

overview_rows = database.select('overview',
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

database.disconnect()
database.connect('restore')

print(f'Updating {len(overview_rows)} overviews')

for i, row in enumerate(overview_rows):
    print(f'  Updating overview {i}')
    if row['first_seen_date'] >= restore_date:
        database.insert('overview', {
            'bus_number': row['bus_number'],
            'first_seen_date': row['first_seen_date'],
            'first_seen_system_id': row['first_seen_system_id'],
            'last_seen_date': row['last_seen_date'],
            'last_seen_system_id': row['last_seen_system_id']
        })
    else:
        database.update('overview',
            values={
                'last_seen_date': row['last_seen_date'],
                'last_seen_system_id': row['last_seen_system_id']
            },
            filters={
                'bus_number': row['bus_number']
            })

database.commit()
database.disconnect()
database.connect('bctracker')

record_rows = database.select('record', 
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
    trip_record_rows = database.select('trip_record',
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
    first_overview_rows = database.select('overview',
        columns={
            'overview.bus_number': 'bus_number'
        },
        filters={
            'overview.first_record_id': row['id']
        })
    last_overview_rows = database.select('overview',
        columns={
            'overview.bus_number': 'bus_number'
        },
        filters={
            'overview.last_record_id': row['id']
        })
    database.disconnect()
    database.connect('restore')
    new_id = database.insert('record', {
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
        database.insert('trip_record', {
            'record_id': new_id,
            'trip_id': trip_row['trip_id']
        })
    for overview_row in first_overview_rows:
        database.update('overview',
            values={
                'first_record_id': new_id
            },
            filters={
                'overview.bus_number': overview_row['bus_number']
            })
    for overview_row in last_overview_rows:
        database.update('overview',
            values={
                'last_record_id': new_id
            },
            filters={
                'overview.bus_number': overview_row['bus_number']
            })
    database.commit()
    database.disconnect()
    database.connect('bctracker')

transfer_rows = database.select('transfer',
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

database.disconnect()
database.connect('restore')

print(f'Moving {len(transfer_rows)} transfers')

for i, row in enumerate(transfer_rows):
    print(f'  Moving transfer {i}')
    database.insert('transfer', row)

database.commit()
database.disconnect()
