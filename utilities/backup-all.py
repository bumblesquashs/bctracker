#!/usr/bin/env python

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import backup

date = datetime.now() - timedelta(days=1)
while date >= datetime(2020, 1, 1):
    backup.run(date, False)
    date = date - timedelta(days=1)
