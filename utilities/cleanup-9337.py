#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

database = Database()
database.connect()

allocation_rows = database.select(
    table='allocation',
    columns=[
        'allocation_id'
    ],
    filters={
        'vehicle_id': '9337'
    },
    order_by='allocation_id ASC',
    limit=1
)
allocation_id = allocation_rows[0]['allocation_id']

database.execute(
    '''
    DELETE FROM transfer
    WHERE old_allocation_id IN (
        SELECT allocation_id FROM allocation WHERE vehicle_id = '9337'
    )
    '''
)

database.execute(
    '''
    DELETE FROM trip_record
    WHERE record_id IN (
        SELECT r.record_id FROM record r
        JOIN allocation a ON a.allocation_id = r.allocation_id
        WHERE a.system_id = 'whistler' AND a.vehicle_id = '9337'
    )
    '''
)

database.execute(
    '''
    DELETE FROM allocation_record
    WHERE allocation_id IN (
        SELECT allocation_id FROM allocation WHERE vehicle_id = '9337'
    )
    '''
)

database.execute(
    '''
    DELETE FROM record
    WHERE allocation_id IN (
        SELECT allocation_id FROM allocation WHERE system_id = 'whistler' AND vehicle_id = '9337'
    )
    '''
)

database.execute(
    '''
    DELETE FROM assignment
    WHERE allocation_id IN (
        SELECT allocation_id FROM allocation WHERE vehicle_id = '9337'
    )
    '''
)

database.execute(
    '''
    UPDATE record
    SET allocation_id = ?
    WHERE allocation_id IN (
        SELECT allocation_id FROM allocation WHERE vehicle_id = '9337'
    )
    ''',
    [allocation_id]
)

database.execute(
    '''
    DELETE FROM allocation
    WHERE vehicle_id = '9337' AND allocation_id != ?
    ''',
    [allocation_id]
)

first_record_rows = database.select(
    table='record',
    columns=[
        'record_id'
    ],
    filters={
        'allocation_id': allocation_id
    },
    order_by='date ASC, record_id ASC',
    limit=1
)
first_record = first_record_rows[0]

last_record_rows = database.select(
    table='record',
    columns=[
        'record_id',
        'date'
    ],
    filters={
        'allocation_id': allocation_id
    },
    order_by='date DESC, record_id DESC',
    limit=1
)
last_record = last_record_rows[0]

database.insert(
    table='allocation_record',
    values={
        'allocation_id': allocation_id,
        'first_record_id': first_record['record_id'],
        'last_record_id': last_record['record_id']
    }
)

database.update(
    table='allocation',
    values={
        'last_seen': last_record['date'],
        'active': 1
    }
)

database.commit()
database.disconnect()
