
from models.system import get_system

class Transfer:
    def __init__(self, transfer_id, bus, date, old_system_id, new_system_id):
        self.id = transfer_id
        self.bus = bus
        self.date = date
        self.old_system_id = old_system_id
        self.new_system_id = new_system_id
    
    @property
    def old_system(self):
        return get_system(self.old_system_id)
    
    @property
    def new_system(self):
        return get_system(self.new_system_id)
