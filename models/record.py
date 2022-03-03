
from models.bus import Bus
from models.system import get_system
from models.time import Time

import formatting

class Record:
    ID_COLUMN = 'record_id'
    BUS_NUMBER_COLUMN = 'record_bus_number'
    DATE_COLUMN = 'record_date'
    SYSTEM_ID_COLUMN = 'record_system_id'
    BLOCK_ID_COLUMN = 'record_block_id'
    ROUTES_COLUMN = 'record_routes'
    START_TIME_COLUMN = 'record_start_time'
    END_TIME_COLUMN = 'record_end_time'
    FIRST_SEEN_COLUMN = 'record_first_seen'
    LAST_SEEN_COLUMN = 'record_last_seen'
    
    def __init__(self, row):
        self.id = row[self.ID_COLUMN]
        self.bus = Bus(row[self.BUS_NUMBER_COLUMN])
        self.date = formatting.database(row[self.DATE_COLUMN])
        self.system_id = row[self.SYSTEM_ID_COLUMN]
        self.block_id = row[self.BLOCK_ID_COLUMN]
        self.routes = row[self.ROUTES_COLUMN]
        self.start_time = Time(row[self.START_TIME_COLUMN])
        self.end_time = Time(row[self.END_TIME_COLUMN])
        self.first_seen = Time(row[self.FIRST_SEEN_COLUMN])
        self.last_seen = Time(row[self.LAST_SEEN_COLUMN])
    
    @property
    def system(self):
        return get_system(self.system_id)
    
    @property
    def is_available(self):
        return self.block is not None
    
    @property
    def block(self):
        return self.system.get_block(self.block_id)
