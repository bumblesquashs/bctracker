#!/usr/bin/env python
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect()

bus_numbers_data = database.execute('SELECT DISTINCT bus_number FROM records')

for bus_number_data in bus_numbers_data:
    bus_number = bus_number_data[0]
    records_data = database.select('records', 
        columns=['date', 'system_id'],
        filters={
            'bus_number': bus_number
        },
        order_by='record_id')
    for (i, data) in enumerate(records_data):
        if i == 0:
            continue
        old_system_id = records_data[i - 1]['system_id']
        new_system_id = data['system_id']
        if new_system_id != old_system_id:
            database.insert('transfers', {
                'bus_number': bus_number,
                'date': data['date'],
                'old_system_id': old_system_id,
                'new_system_id': new_system_id
            })

database.commit()
database.disconnect()
