import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect()

database.execute('''
    CREATE TABLE records (
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

database.execute('CREATE INDEX records_bus_number ON records (bus_number)')

database.commit()
database.disconnect()