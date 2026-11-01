#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database import Database

database = Database()
database.connect()
database.execute("UPDATE allocation SET vehicle_id = CONCAT(vehicle_id, '-1') WHERE vehicle_id >= '8000' AND vehicle_id < '9000' AND agency_id = 'bc-transit'")
database.commit()
database.disconnect()
