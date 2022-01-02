#!/usr/bin/env python
import os
from zipfile import ZipFile
from glob import glob
from datetime import datetime, timedelta
from pathlib import Path

CWD = os.path.dirname(Path(os.path.abspath(__file__)).parent.absolute())

date = datetime.now().replace(day=1) - timedelta(days=1)

while date >= datetime(2020, 1, 1):
    formatted_date = date.strftime('%Y-%m')
    gtfs_files = glob(f'{CWD}/archives/gtfs/*_{formatted_date}-*.zip')
    realtime_files = glob(f'{CWD}/archives/realtime/*_{formatted_date}-*.bin')
    
    if len(gtfs_files) > 0 or len(realtime_files) > 0:
        with ZipFile(f'{CWD}/backups/{formatted_date}.zip', 'w') as zip:
            zip.write(f'{CWD}/archives/bctracker.db', 'bctracker.db')
            for file in gtfs_files:
                zip.write(file, file[len(f'{CWD}/archives/'):])
                os.remove(file)
            for file in realtime_files:
                zip.write(file, file[len(f'{CWD}/archives/'):])
                os.remove(file)
    date = date.replace(day=1) - timedelta(days=1)
