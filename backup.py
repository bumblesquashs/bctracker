#!/usr/bin/env python

import os
from zipfile import ZipFile
from glob import glob

import database

def run(date, include_db):
    if include_db:
        database.backup()
    
    formatted_date = date.strftime('%Y-%m-%d')
    
    gtfs_files = glob(f'archives/gtfs/*_{formatted_date}.zip')
    realtime_files = glob(f'archives/realtime/*_{formatted_date}-*.bin')
    
    if len(gtfs_files) > 0 or len(realtime_files) > 0:
        print(f'Creating backup for {formatted_date} ({len(gtfs_files)} GTFS, {len(realtime_files)} RT)')
        with ZipFile(f'backups/{formatted_date}.zip', 'w') as zip:
            if include_db:
                zip.write('archives/bctracker.db', 'bctracker.db')
            for file in gtfs_files:
                zip.write(file, file[len('archives/'):])
                os.remove(file)
            for file in realtime_files:
                zip.write(file, file[len('archives/'):])
                os.remove(file)
