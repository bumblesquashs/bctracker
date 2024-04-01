#!/usr/bin/env python

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect(foreign_keys=False)

database.execute("DELETE FROM departure WHERE system_id = 'broome-county'")
database.execute("DELETE FROM point WHERE system_id = 'broome-county'")
database.execute("DELETE FROM route WHERE system_id = 'broome-county'")
database.execute("DELETE FROM stop WHERE system_id = 'broome-county'")
database.execute("DELETE FROM trip WHERE system_id = 'broome-county'")

database.commit()
database.disconnect()
