#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

database = Database()

database.connect()

database.execute('ALTER TABLE overview ADD yard_number TEXT')

database.commit()
database.disconnect()
