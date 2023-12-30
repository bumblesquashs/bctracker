#!/usr/bin/env python

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import backup

from models.date import Date

date = Date.today().previous()
end_date = Date(2020, 1, 1)
while date >= end_date:
    backup.run(date, False)
    date = date.previous()
