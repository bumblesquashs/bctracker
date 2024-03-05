#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect(foreign_keys=False)

database.execute('ALTER TABLE record RENAME TO record_old')
database.execute('ALTER TABLE transfer RENAME TO transfer_old')
database.execute('ALTER TABLE overview RENAME TO overview_old')

database.execute('DROP TABLE position')
database.execute('DROP TABLE route')
database.execute('DROP TABLE stop')
database.execute('DROP TABLE trip')
database.execute('DROP TABLE departure')
database.execute('DROP TABLE point')

for sql in database.SQL_SCRIPTS:
    database.execute(sql)

database.execute('''
    INSERT INTO record (record_id, agency_id, bus_number, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen)
    SELECT record_id, 'bc-transit', bus_number, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen
    FROM record_old
''')

database.execute('''
    INSERT INTO transfer (transfer_id, agency_id, bus_number, date, old_system_id, new_system_id)
    SELECT transfer_id, 'bc-transit', bus_number, date, old_system_id, new_system_id
    FROM transfer_old
''')

database.execute('''
    INSERT INTO overview (agency_id, bus_number, first_seen_date, first_seen_system_id, first_record_id, last_seen_date, last_seen_system_id, last_record_id)
    SELECT 'bc-transit', bus_number, first_seen_date, first_seen_system_id, first_record_id, last_seen_date, last_seen_system_id, last_record_id
    FROM overview_old
''')

database.execute('DROP TABLE record_old')
database.execute('DROP TABLE transfer_old')
database.execute('DROP TABLE overview_old')

database.commit()
database.disconnect()
