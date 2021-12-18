#!/usr/bin/env python

import os
import sqlite3
from zipfile import ZipFile
from glob import glob
from datetime import datetime

CWD = os.path.dirname(__file__)

connection = sqlite3.connect(f'{CWD}/data/bctracker.db')
backup = sqlite3.connect(f'{CWD}/archives/bctracker.db')
connection.backup(backup)
connection.close()
backup.close()

formatted_date = datetime.now().strftime('%Y-%m')

with ZipFile(f'{CWD}/backups/{formatted_date}.zip', 'w') as zip:
    zip.write('{CWD}/archives/bctracker.db', 'bctracker.db')
    for file in glob(f'{CWD}/archives/gtfs/*_{formatted_date}-*.zip'):
        zip.write(file, file[len(f'{CWD}/archives/'):])
    for file in glob(f'{CWD}/archives/realtime/*_{formatted_date}-*.bin'):
        zip.write(file, file[len(f'{CWD}/archives/'):])
