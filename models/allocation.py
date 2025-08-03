
from dataclasses import dataclass

from models.agency import Agency
from models.bus import Bus
from models.context import Context
from models.date import Date
from models.record import Record
from models.row import Row
from models.system import System
from models.time import Time

import repositories

@dataclass(slots=True)
class Allocation:
    
    id: int
    agency: Agency
    bus: Bus
    system: System | None
    first_seen: Date
    first_record: Record | None
    last_seen: Date
    last_record: Record | None
    active: bool
    records_count: int
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    @property
    def context(self):
        return Context(self.agency, self.system)
    
    @property
    def first_date(self):
        if self.first_record:
            return self.first_record.date
        return self.first_seen
    
    @property
    def first_time(self):
        if self.first_record:
            return self.first_record.first_seen
        return Time.unknown(self.context.timezone)
    
    @property
    def last_date(self):
        if self.last_record:
            return self.last_record.date
        return self.last_seen
    
    @property
    def last_time(self):
        if self.last_record:
            return self.last_record.last_seen
        return Time.unknown(self.context.timezone)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.first_seen < other.first_seen
    
    @classmethod
    def from_db(cls, row: Row):
        id = row['id']
        agency = repositories.agency.find(row['agency_id'])
        bus = repositories.order.find_bus(agency.context, row['vehicle_id'])
        system = repositories.system.find(row['system_id'])
        context = Context(agency, system)
        first_seen = Date.parse(row['first_seen'], context.timezone)
        if 'first_record_id' in row:
            row.values['first_record_allocation_id'] = id
            row.values['first_record_agency_id'] = agency.id
            row.values['first_record_vehicle_id'] = bus.id
            row.values['first_record_system_id'] = system.id if system else None
            first_record = row.obj('first_record', Record.from_db)
        else:
            first_record = None
        last_seen = Date.parse(row['last_seen'], context.timezone)
        if 'last_record_id' in row:
            row.values['last_record_allocation_id'] = id
            row.values['last_record_agency_id'] = agency.id
            row.values['last_record_vehicle_id'] = bus.id
            row.values['last_record_system_id'] = system.id if system else None
            last_record = row.obj('last_record', Record.from_db)
        else:
            last_record = None
        active = row['active'] == 1
        records_count = row['records_count']
        return cls(id, agency, bus, system, first_seen, first_record, last_seen, last_record, active, records_count)
