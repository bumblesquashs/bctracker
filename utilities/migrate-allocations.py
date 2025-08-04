#!/usr/bin/env python

# Migration from overviews to allocations

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
            'active': 1
        }
    )

new_db.commit()

date_range = DateRange(Date(2020, 1, 1, DEFAULT_TIMEZONE), Date.today())

unexpected_updates = []

for date in date_range:
    print(f'Migrating data for {date.format_long()}')
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
        
        # Assumption: Buses have only ever been transferred once in a day, before any records are created on that day
        # This means we can and should update transfers FIRST
        for row in transfer_rows:
            vehicle_id = str(row['bus_number'])
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
                    'active': 1
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
                        'active': 1
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
    new_db.commit()

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
                'active': 1
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

new_db.commit()

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

new_db.commit()

old_db.disconnect()
new_db.disconnect()
