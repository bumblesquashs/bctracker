import database

database.connect()

database.execute('''
    CREATE TABLE bus_history (
        bus_number INTEGER,
        date TEXT,
        system_id TEXT,
        feed_version TEXT,
        block_id TEXT,
        routes TEXT,
        start_time TEXT,
        end_time TEXT
    )
''')

database.disconnect()