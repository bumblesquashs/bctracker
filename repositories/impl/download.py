
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.date import Date
from models.download import DownloadTrigger
from models.time import Time

@dataclass(slots=True)
class DownloadRepository:
    
    database: Database
    
    def create(self, context: Context, date: Date, time: Time, trigger: DownloadTrigger):
        '''Inserts a new download into the database'''
        return self.database.insert(
            table='download',
            values={
                'agency_id': context.agency_id,
                'system_id': context.system_id,
                'date': date.format_db(),
                'time': time.format_db(),
                'trigger': trigger.value
            }
        )
