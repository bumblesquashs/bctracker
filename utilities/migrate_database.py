import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect()

database.execute('''
    CREATE TABLE IF NOT EXISTS new_records (
        record_id INTEGER PRIMARY KEY ASC,
        bus_number INTEGER NOT NULL,
        date TEXT NOT NULL,
        system_id TEXT NOT NULL,
        block_id TEXT NOT NULL,
        routes TEXT NOT NULL,
        start_time TEXT,
        end_time TEXT,
        first_seen TEXT,
        last_seen TEXT
    )
''')

database.execute('''
    INSERT INTO new_records (bus_number, date, system_id, block_id, routes, start_time, end_time)
    SELECT bus_number, date, system_id, block_id, routes, start_time, end_time
    FROM records
''')

database.execute('DROP TABLE records')

database.execute('ALTER TABLE new_records RENAME TO records')

database.commit()
database.disconnect()