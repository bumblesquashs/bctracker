#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect(foreign_keys=False)

database.execute('''
    ALTER TABLE position ADD sequence INTEGER;
''')

database.commit()
database.disconnect()
