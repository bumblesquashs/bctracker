#!/usr/bin/env python

import os
import sqlite3
from zipfile import ZipFile
from glob import glob
from datetime import datetime, timedelta

CWD = os.path.dirname(os.path.abspath(__file__))

connection = sqlite3.connect(f'{CWD}/data/bctracker.db')
backup = sqlite3.connect(f'{CWD}/archives/bctracker.db')
connection.backup(backup)
connection.close()
backup.close()

date = datetime.now().replace(day=1) - timedelta(days=1)
formatted_date = date.strftime('%Y-%m')

with ZipFile(f'{CWD}/backups/{formatted_date}.zip', 'w') as zip:
    zip.write(f'{CWD}/archives/bctracker.db', 'bctracker.db')
    for file in glob(f'{CWD}/archives/gtfs/*_{formatted_date}-*.zip'):
        zip.write(file, file[len(f'{CWD}/archives/'):])
        os.remove(file)
    for file in glob(f'{CWD}/archives/realtime/*_{formatted_date}-*.bin'):
        zip.write(file, file[len(f'{CWD}/archives/'):])
        os.remove(file)
