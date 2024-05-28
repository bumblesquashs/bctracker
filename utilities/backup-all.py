#!/usr/bin/env python

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models.date import Date

from database import Database
from settings import Settings
from services.default import DefaultBackupService

backup_service = DefaultBackupService(
    database=Database(),
    settings=Settings()
)

date = Date.today().previous()
end_date = Date(2020, 1, 1)
while date >= end_date:
    backup_service.run(date, include_db=False)
    date = date.previous()
