import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect()

database.execute('ALTER TABLE records ADD COLUMN first_seen TEXT')
database.execute('ALTER TABLE records ADD COLUMN last_seen TEXT')

database.commit()
database.disconnect()