#!/usr/bin/env python

# Migration from overviews to allocations

# How it works:
# 1. Load old overviews
# 2. For each old overview, create an allocation based on the first seen system
# 3. Create a date range from Jan 1 2025 to the current date
# 4. For each day in that date range, migrate any records, creating new allocations as needed
# 5. For each old overview, create another allocation if the last seen system doesn't match the last allocation
# 6. For each allocation, create allocation/record references

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database
from constants import DEFAULT_TIMEZONE

from models.date import Date
from models.daterange import DateRange

old_db = Database('abtracker remote')
new_db = Database('abtracker')

old_db.connect(run_scripts=False)
new_db.connect()

unexpected_updates = []

overview_rows = old_db.select(
    table='overview',
    columns=[
        'agency_id',
        'bus_number',
        'first_seen_date',
        'first_seen_system_id',
        'first_record_id',
        'last_seen_date',
        'last_seen_system_id',
        'last_record_id'
    ]
)

for row in overview_rows:
    new_db.insert(
        table='allocation',
        values={
            'agency_id': row['agency_id'],
            'vehicle_id': str(row['bus_number']),
            'system_id': row['first_seen_system_id'],
            'first_seen': row['first_seen_date'],
            'last_seen': row['first_seen_date'],
            'active': 1,
            'last_lat': None,
            'last_lon': None,
            'last_stop_id': None,
            'last_stop_number': None,
            'last_stop_name': None
        }
    )

def migrate_records(date: Date):
    record_rows = old_db.select(
        table='record',
        columns=[
            'agency_id',
            'bus_number',
            'system_id',
            'block_id',
            'routes',
            'start_time',
            'end_time',
            'first_seen',
            'last_seen'
        ],
        filters={
            'date': date.format_db()
        },
        order_by='record_id'
    )
    if record_rows:
        print(f'  Records: {len(record_rows)}')
        
        for row in record_rows:
            agency_id = row['agency_id']
            vehicle_id = str(row['bus_number'])
            system_id = row['system_id']
            
            allocation_rows = new_db.select(
                table='allocation',
                columns=[
                    'allocation_id'
                ],
                filters={
                    'agency_id': agency_id,
                    'vehicle_id': vehicle_id,
                    'system_id': system_id,
                    'active': 1
                },
                limit=1
            )
            if allocation_rows:
                allocation_id = allocation_rows[0]['allocation_id']
            else:
                allocation_id = new_db.insert(
                    table='allocation',
                    values={
                        'agency_id': agency_id,
                        'vehicle_id': vehicle_id,
                        'system_id': system_id,
                        'first_seen': date.format_db(),
                        'last_seen': date.format_db(),
                        'active': 1,
                        'last_lat': None,
                        'last_lon': None,
                        'last_stop_id': None,
                        'last_stop_number': None,
                        'last_stop_name': None
                    }
                )
            
            new_db.update(
                table='allocation',
                values={
                    'last_seen': date.format_db()
                },
                filters={
                    'allocation_id': allocation_id
                }
            )
            
            previous_records = new_db.select(
                table='record',
                columns=[
                    'record_id'
                ],
                filters={
                    'allocation_id': allocation_id,
                    'date': date.format_db(),
                    'block_id': row['block_id']
                }
            )
            if previous_records:
                new_db.update(
                    table='record',
                    values={
                        'last_seen': row['last_seen']
                    },
                    filters={
                        'record_id': previous_records[0]['record_id']
                    }
                )
            else:
                new_db.insert(
                    table='record',
                    values={
                        'allocation_id': allocation_id,
                        'date': date.format_db(),
                        'block_id': row['block_id'],
                        'route_numbers': row['routes'],
                        'start_time': row['start_time'],
                        'end_time': row['end_time'],
                        'first_seen': row['first_seen'],
                        'last_seen': row['last_seen']
                    }
                )

date_range = DateRange(Date(2025, 1, 1, DEFAULT_TIMEZONE), Date.today())
for date in date_range:
    print(f'Migrating data for {date.format_long()}')
    
    migrate_records(date)

print('Creating allocation_record entries')
allocation_ids = new_db.select(
    table='allocation',
    columns=[
        'allocation_id'
    ],
    initializer=lambda r: r['allocation_id']
)
for allocation_id in allocation_ids:
    record_ids = new_db.select(
        table='record',
        columns=[
            'record_id'
        ],
        filters={
            'allocation_id': allocation_id
        },
        order_by={
            'date': 'ASC',
            'record_id': 'ASC'
        },
        initializer=lambda r: r['record_id']
    )
    if record_ids:
        new_db.insert(
            table='allocation_record',
            values={
                'allocation_id': allocation_id,
                'first_record_id': record_ids[0],
                'last_record_id': record_ids[-1]
            }
        )

for update in unexpected_updates:
    print(update)

new_db.commit()

old_db.disconnect()
new_db.disconnect()
