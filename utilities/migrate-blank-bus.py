#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

database = Database()
database.connect()
database.execute("UPDATE allocation SET vehicle_id = '0' WHERE vehicle_id = ''")
database.commit()
database.disconnect()
