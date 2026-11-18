#!/usr/bin/env python

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models.date import Date
from models.province import Province

from database import Database
from settings import Settings
from services.impl import BackupService

backup_service = BackupService(
    database=Database(),
    settings=Settings()
)

timezone = Province.BC.default_timezone
date = Date.today(timezone).previous()
end_date = Date(2020, 1, 1, timezone)
while date >= end_date:
    backup_service.run(date, include_db=False)
    date = date.previous()
