#!/usr/bin/env python

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models.date import Date

from database import Database
from services.impl import BackupService

import settings

backup_service = BackupService(
    database=Database(),
)

province = settings.current.province
date = Date.today(province.default_timezone).previous()
end_date = Date(2020, 1, 1, province.default_timezone)
while date >= end_date:
    backup_service.run(date, include_db=False)
    date = date.previous()
