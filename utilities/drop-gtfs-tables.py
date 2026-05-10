#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

database = Database()
database.connect()

database.execute("DROP TABLE point")
database.execute("DROP TABLE departure")
database.execute("DROP TABLE trip")
database.execute("DROP TABLE stop")
database.execute("DROP TABLE route")

database.commit()
database.disconnect()
