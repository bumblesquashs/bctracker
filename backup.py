#!/usr/bin/env python

import os
from zipfile import ZipFile
from glob import glob

from di import di

from models.date import Date

from services import Config, Database

def run(date, include_db=False, db_name='bctracker', delete_files=True):
    '''Zips all archives from the given date into a single file'''
    config = di[Config]
    formatted_date = date.format_db()
    
    gtfs_files = glob(f'archives/gtfs/*_{formatted_date}.zip')
    realtime_files = glob(f'archives/realtime/*_{formatted_date}-*.bin')
    
    if len(gtfs_files) > 0 or len(realtime_files) > 0 or include_db:
        print(f'Creating backup for {formatted_date} ({len(gtfs_files)} GTFS, {len(realtime_files)} RT, {"DB" if include_db else "no DB"})')
        with ZipFile(f'backups/{formatted_date}.zip', 'w') as zip:
            if config.enable_database_backups and include_db:
                zip.write(f'archives/{db_name}.db', f'{db_name}.db')
            if config.enable_gtfs_backups:
                for file in gtfs_files:
                    zip.write(file, file[len('archives/'):])
                    if delete_files:
                        os.remove(file)
            if config.enable_realtime_backups:
                for file in realtime_files:
                    zip.write(file, file[len('archives/'):])
                    if delete_files:
                        os.remove(file)

if __name__ == '__main__':
    di.add(Config())
    Database().archive()
    date = Date.today()
    run(date, include_db=True, delete_files=False)
