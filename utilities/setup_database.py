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
        end_time TEXT
    )
''')

database.disconnect()