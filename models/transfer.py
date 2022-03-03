
from models.bus import Bus
from models.system import get_system

import formatting

class Transfer:
    ID_COLUMN = 'transfer_id'
    BUS_NUMBER_COLUMN = 'transfer_bus_number'
    DATE_COLUMN = 'transfer_date'
    OLD_SYSTEM_ID_COLUMN = 'transfer_old_system_id'
    NEW_SYSTEM_ID_COLUMN = 'transfer_new_system_id'
    
    def __init__(self, row):
        self.id = row[self.ID_COLUMN]
        self.bus = Bus(row[self.BUS_NUMBER_COLUMN])
        self.date = formatting.database(row[self.DATE_COLUMN])
        self.old_system_id = row[self.OLD_SYSTEM_ID_COLUMN]
        self.new_system_id = row[self.NEW_SYSTEM_ID_COLUMN]
    
    @property
    def old_system(self):
        return get_system(self.old_system_id)
    
    @property
    def new_system(self):
        return get_system(self.new_system_id)
