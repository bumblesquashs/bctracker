#!/usr/bin/env python

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models.date import Date

from config import Config
from database import Database
from services.backup import DefaultBackupService

backup_service = DefaultBackupService(
    config=Config(),
    database=Database()
)

date = Date.today().previous()
end_date = Date(2020, 1, 1)
while date >= end_date:
    backup_service.run(date, include_db=False)
    date = date.previous()
