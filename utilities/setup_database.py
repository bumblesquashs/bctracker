#!/usr/bin/env python
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect()

database.execute('''
    CREATE TABLE IF NOT EXISTS records (
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
    CREATE TABLE IF NOT EXISTS trip_records (
        trip_record_id INTEGER PRIMARY KEY ASC,
        record_id INTEGER NOT NULL,
        trip_id TEXT NOT NULL,
        FOREIGN KEY (record_id) REFERENCES records (record_id)
    )
''')

database.execute('''
    CREATE TABLE IF NOT EXISTS transfers (
        transfer_id INTEGER PRIMARY KEY ASC,
        bus_number INTEGER NOT NULL,
        date TEXT NOT NULL,
        old_system_id TEXT NOT NULL,
        new_system_id TEXT NOT NULL
    )
''')

database.execute('CREATE INDEX IF NOT EXISTS records_bus_number ON records (bus_number)')
database.execute('CREATE INDEX IF NOT EXISTS trip_records_record_id ON trip_records (record_id)')
database.execute('CREATE INDEX IF NOT EXISTS transfers_bus_number ON transfers (bus_number)')

database.commit()
database.disconnect()