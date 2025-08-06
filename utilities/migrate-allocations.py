#!/usr/bin/env python

# Migration from overviews to allocations

# How it works:
# 1. Load old overviews
# 2. For each old overview, create an allocation based on the first seen system
# 3. Create a date range from Jan 1 2020 to the current date
# 4. For each day in that date range, migrate any transfers and records, creating new allocations as needed
# 5. For each old overview, create another allocation if the last seen system doesn't match the last allocation
# 6. For each allocation, create allocation/record references

# Exceptions:
# 1. A couple of transfers are missing; while these could be generated automatically through the fallback, the dates may be incorrect
#      3029: West Kootenay -> East Kootenay on 2023-03-03
#      9386: Comox -> Cowichan on 2023-08-28
#      9298: Whistler -> Pemberton on 2023-09-11
#      2804: North Okanagan -> Quesnel on 2023-09-28
#      2805: North Okanagan -> Quesnel on 2023-09-28
#      9260: Kelowna -> Kamloops on 2023-12-12
#      2620: North Okanagan -> Kamloops on 2023-12-22
# 2. Generally we assume that any transfers for a bus on any given day occurred before its first record, so it's safe to migrate those first.
#    However, there's a couple of cases of buses that mistakenly logged in to the wrong system and created a record, then were "transferred" to the right system and made another record.
#    This has happened for:
#      2520: Sunshine Coast -> Mount Waddington on 2023-11-15
#      1261: Victoria -> Fraser Valley on 2025-02-05
#    For these cases, we can skip the transfers migration and rely on the fallback to auto-create transfers

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database
from constants import DEFAULT_TIMEZONE

from models.date import Date
from models.daterange import DateRange

old_db = Database('bctracker-old')
new_db = Database('bctracker-new')

old_db.connect(run_scripts=False)
new_db.connect()

unexpected_updates = []

# Exception 1 - see notes at top of file
old_db.insert(
    table='transfer',
    values={
        'bus_number': 3029,
        'date': '2023-03-03',
        'old_system_id': 'west-kootenay',
        'new_system_id': 'east-kootenay'
    }
)
old_db.insert(
    table='transfer',
    values={
        'bus_number': 9386,
        'date': '2023-08-28',
        'old_system_id': 'comox',
        'new_system_id': 'cowichan-valley'
    }
)
old_db.insert(
    table='transfer',
    values={
        'bus_number': 9298,
        'date': '2023-09-11',
        'old_system_id': 'whistler',
        'new_system_id': 'pemberton'
    }
)
old_db.insert(
    table='transfer',
    values={
        'bus_number': 2804,
        'date': '2023-09-28',
        'old_system_id': 'north-okanagan',
        'new_system_id': 'quesnel'
    }
)
old_db.insert(
    table='transfer',
    values={
        'bus_number': 2805,
        'date': '2023-09-28',
        'old_system_id': 'north-okanagan',
        'new_system_id': 'quesnel'
    }
)
old_db.insert(
    table='transfer',
    values={
        'bus_number': 9260,
        'date': '2023-12-12',
        'old_system_id': 'kelowna',
        'new_system_id': 'kamloops'
    }
)
old_db.insert(
    table='transfer',
    values={
        'bus_number': 2620,
        'date': '2023-12-22',
        'old_system_id': 'north-okanagan',
        'new_system_id': 'kamloops'
    }
)

overview_rows = old_db.select(
    table='overview',
    columns=[
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
            'agency_id': 'bc-transit',
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

def migrate_transfers(date: Date):
    transfer_rows = old_db.select(
        table='transfer',
        columns=[
            'bus_number',
            'old_system_id',
            'new_system_id'
        ],
        filters={
            'date': date.format_db()
        }
    )
    if transfer_rows:
        print(f'  Transfers: {len(transfer_rows)}')
        for row in transfer_rows:
            vehicle_id = str(row['bus_number'])
            # Exception 2 - see notes at top of file
            if (vehicle_id == '2520' and date.format_db() == '2023-11-15') or (vehicle_id == '1261' and date.format_db() == '2025-02-05'):
                continue
            
            old_allocation_id = new_db.select(
                table='allocation',
                columns=[
                    'allocation_id'
                ],
                filters={
                    'agency_id': 'bc-transit',
                    'vehicle_id': vehicle_id,
                    'system_id': row['old_system_id'],
                    'active': 1
                },
                limit=1,
                initializer=lambda r: r['allocation_id']
            )[0]
            
            new_db.update(
                table='allocation',
                values={
                    'active': 0
                },
                filters={
                    'allocation_id': old_allocation_id
                }
            )
            new_allocation_id = new_db.insert(
                table='allocation',
                values={
                    'agency_id': 'bc-transit',
                    'vehicle_id': vehicle_id,
                    'system_id': row['new_system_id'],
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
            new_db.insert(
                table='transfer',
                values={
                    'date': date.format_db(),
                    'old_allocation_id': old_allocation_id,
                    'new_allocation_id': new_allocation_id
                }
            )

def migrate_records(date: Date):
    record_rows = old_db.select(
        table='record',
        columns=[
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
            vehicle_id = str(row['bus_number'])
            system_id = row['system_id']
            
            allocation_row = new_db.select(
                table='allocation',
                columns=[
                    'allocation_id',
                    'system_id'
                ],
                filters={
                    'agency_id': 'bc-transit',
                    'vehicle_id': vehicle_id,
                    'active': 1
                },
                limit=1
            )[0]
            allocation_id = allocation_row['allocation_id']
            allocation_system_id = allocation_row['system_id']
            
            if system_id == allocation_system_id:
                new_db.update(
                    table='allocation',
                    values={
                        'last_seen': date.format_db()
                    },
                    filters={
                        'allocation_id': allocation_id
                    }
                )
            else:
                # Fallback - this basically means the record is in a new system but there wasn't a transfer in the DB
                # This may have happened sometimes when transfers were created based on records and not just when online
                unexpected_updates.append(f'{date.format_db()}: Transfer of {vehicle_id} from {allocation_system_id} to {system_id}')
                new_db.update(
                    table='allocation',
                    values={
                        'active': 0
                    },
                    filters={
                        'allocation_id': allocation_id
                    }
                )
                old_allocation_id = allocation_id
                allocation_id = new_db.insert(
                    table='allocation',
                    values={
                        'agency_id': 'bc-transit',
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
                new_db.insert(
                    table='transfer',
                    values={
                        'date': date.format_db(),
                        'old_allocation_id': old_allocation_id,
                        'new_allocation_id': allocation_id
                    }
                )
            
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

date_range = DateRange(Date(2020, 1, 1, DEFAULT_TIMEZONE), Date.today())
for date in date_range:
    print(f'Migrating data for {date.format_long()}')
    
    migrate_transfers(date)
    migrate_records(date)

for row in overview_rows:
    vehicle_id = str(row['bus_number'])
    last_seen = row['last_seen_date']
    system_id = row['last_seen_system_id']
    allocation_row = new_db.select(
        table='allocation',
        columns=[
            'allocation_id',
            'system_id'
        ],
        filters={
            'agency_id': 'bc-transit',
            'vehicle_id': vehicle_id,
            'active': 1
        },
        limit=1
    )[0]
    allocation_id = allocation_row['allocation_id']
    allocation_system_id = allocation_row['system_id']
    if system_id == allocation_system_id:
        new_db.update(
            table='allocation',
            values={
                'last_seen': last_seen
            },
            filters={
                'allocation_id': allocation_id
            }
        )
    else:
        # Fallback - this basically means the bus has been seen in a new system but doesn't have any records there yet and no transfer was created for some reason
        unexpected_updates.append(f'Last seen transfer of {vehicle_id} from {allocation_system_id} to {system_id}')
        new_db.update(
            table='allocation',
            values={
                'active': 0
            },
            filters={
                'allocation_id': allocation_id
            }
        )
        old_allocation_id = allocation_id
        allocation_id = new_db.insert(
            table='allocation',
            values={
                'agency_id': 'bc-transit',
                'vehicle_id': vehicle_id,
                'system_id': system_id,
                'first_seen': row['last_seen_date'],
                'last_seen': row['last_seen_date'],
                'active': 1,
                'last_lat': None,
                'last_lon': None,
                'last_stop_id': None,
                'last_stop_number': None,
                'last_stop_name': None
            }
        )
        new_db.insert(
            table='transfer',
            values={
                'date': row['last_seen_date'],
                'old_allocation_id': old_allocation_id,
                'new_allocation_id': allocation_id
            }
        )

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
