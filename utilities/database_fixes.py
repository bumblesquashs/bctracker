import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect()

database.execute('''
    DELETE FROM records
    WHERE rowid IN (
        WITH numbered_records AS (
            SELECT rowid, bus_number, block_id, start_time, end_time,
                ROW_NUMBER() OVER(PARTITION BY bus_number ORDER BY date DESC, end_time DESC) AS rn
            FROM records
        )
        SELECT r1.rowid
        FROM numbered_records r1
        INNER JOIN numbered_records r2
            ON r1.bus_number = r2.bus_number AND r1.block_id = r2.block_id
        WHERE r1.rn = r2.rn - 1
            AND r1.start_time IS NULL AND r1.end_time IS NULL
    )
''')

database.commit()
database.disconnect()
