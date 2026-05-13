#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

from models.date import Date
from models.daterange import DateRange
from models.time import Time

from constants import DEFAULT_TIMEZONE

database = Database()
database.connect()

date_range = DateRange(Date(2025, 3, 30, DEFAULT_TIMEZONE), Date.today())
# date_range = DateRange(Date(2025, 4, 1, DEFAULT_TIMEZONE), Date(2025, 4, 1, DEFAULT_TIMEZONE))

def update_records(agency_id):
    ACCURATE_SECONDS = agency_id == 'medicine-hat-transit'
    for date in date_range:
        print(f'Updating {agency_id} for {date.format_long()}')
        rows = database.select(
            table='record',
            columns={
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'allocation_record.first_record_id': 'first_record_id',
                'allocation_record.last_record_id': 'last_record_id',
                'record.record_id': 'id',
                'record.allocation_id': 'allocation_id',
                'record.date': 'date',
                'record.block_id': 'block_id',
                'record.route_numbers': 'route_numbers',
                'record.start_time': 'start_time',
                'record.end_time': 'end_time',
                'record.first_seen': 'first_seen',
                'record.last_seen': 'last_seen'
            },
            joins={
                'allocation': {
                    'allocation.allocation_id': 'record.allocation_id'
                },
                'allocation_record': {
                    'allocation_record.allocation_id': 'record.allocation_id'
                }
            },
            filters={
                'allocation.agency_id': agency_id,
                'record.date': date.format_db()
            }
        )
        if len(rows) == 0:
            continue
        vehicle_rows = {}
        for row in rows:
            vehicle_rows.setdefault(row['vehicle_id'], []).append(row)
        
        for (vehicle_id, rows) in vehicle_rows.items():
            print(' -', vehicle_id)
            record_id = rows[0]['id']
            first_record_id = rows[0]['first_record_id']
            last_record_id = rows[0]['last_record_id']
            allocation_id = rows[0]['allocation_id']
            unused_record_ids = {r['id'] for r in rows[1:]}
            
            all_route_numbers = [r['route_numbers'] for r in rows]
            seen_route_numbers = set()
            seen_add = seen_route_numbers.add
            route_numbers = [n for n in all_route_numbers if not (n in seen_route_numbers or seen_add(n))]
            
            start_times = [Time.parse(r['start_time'], accurate_seconds=ACCURATE_SECONDS) for r in rows]
            end_times = [Time.parse(r['end_time'], accurate_seconds=ACCURATE_SECONDS) for r in rows]
            first_seen_times = [Time.parse(r['first_seen'], accurate_seconds=ACCURATE_SECONDS) for r in rows]
            last_seen_times = [Time.parse(r['last_seen'], accurate_seconds=ACCURATE_SECONDS) for r in rows]
            
            start_time = min(start_times)
            end_time = max(end_times)
            first_seen = min(first_seen_times)
            last_seen = max(last_seen_times)
            
            if first_record_id in unused_record_ids:
                database.update(
                    table='allocation_record',
                    values={
                        'first_record_id': record_id
                    },
                    filters={
                        'allocation_id': allocation_id
                    }
                )
            if last_record_id in unused_record_ids:
                database.update(
                    table='allocation_record',
                    values={
                        'last_record_id': record_id
                    },
                    filters={
                        'allocation_id': allocation_id
                    }
                )
            database.update(
                table='trip_record',
                values={
                    'record_id': record_id
                },
                filters={
                    'record_id': unused_record_ids
                }
            )
            database.delete(
                table='record',
                filters={
                    'record_id': unused_record_ids
                }
            )
            database.update(
                table='record',
                values={
                    'block_id': None,
                    'route_numbers': ', '.join(route_numbers),
                    'start_time': start_time.format_db(),
                    'end_time': end_time.format_db(),
                    'first_seen': first_seen.format_db(),
                    'last_seen': last_seen.format_db()
                },
                filters={
                    'record_id': record_id
                }
            )

update_records('roam')
update_records('medicine-hat-transit')

database.commit()
database.disconnect()
