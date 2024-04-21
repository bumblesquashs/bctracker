#!/usr/bin/env python

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.default.connect(foreign_keys=False)

database.default.execute('''
    ALTER TABLE position ADD sequence INTEGER;
''')

database.default.commit()
database.default.disconnect()
