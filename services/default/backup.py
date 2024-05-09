
import os
from zipfile import ZipFile
from glob import glob

from config import Config
from database import Database

from services import BackupService

class DefaultBackupService(BackupService):
    
    __slots__ = (
        'config',
        'database'
    )
    
    def __init__(self, config: Config, database: Database):
        self.config = config
        self.database = database
    
    def run(self, date, include_db=False, delete_files=True):
        '''Zips all archives from the given date into a single file'''
        formatted_date = date.format_db()
        
        gtfs_files = glob(f'archives/gtfs/*_{formatted_date}.zip')
        realtime_files = glob(f'archives/realtime/*_{formatted_date}-*.bin')
        
        if gtfs_files or realtime_files or include_db:
            print(f'Creating backup for {formatted_date} ({len(gtfs_files)} GTFS, {len(realtime_files)} RT, {"DB" if include_db else "no DB"})')
            with ZipFile(f'backups/{formatted_date}.zip', 'w') as zip:
                if self.config.enable_database_backups and include_db:
                    zip.write(f'archives/{self.database.name}.db', f'{self.database.name}.db')
                if self.config.enable_gtfs_backups:
                    for file in gtfs_files:
                        zip.write(file, file[len('archives/'):])
                        if delete_files:
                            os.remove(file)
                if self.config.enable_realtime_backups:
                    for file in realtime_files:
                        zip.write(file, file[len('archives/'):])
                        if delete_files:
                            os.remove(file)

