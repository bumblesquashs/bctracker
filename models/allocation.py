
from dataclasses import dataclass

from models.bus import Bus
from models.context import Context
from models.date import Date
from models.position import Position
from models.record import Record
from models.row import Row
from models.time import Time
from models.timestamp import Timestamp

@dataclass(slots=True)
class Allocation:
    
    id: int
    context: Context
    bus: Bus
    first_seen: Date
    first_record: Record | None
    last_seen: Date
    last_record: Record | None
    active: bool
    last_lat: float | None
    last_lon: float | None
    last_stop_id: str | None
    last_stop_number: str | None
    last_stop_name: str | None
    last_seen_timestamp: Timestamp | None
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
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
    
    @property
    def last_position(self):
        if self.last_lat and self.last_lon:
            return Position(self.context.system, self.bus, lat=self.last_lat, lon=self.last_lon, timestamp=self.last_seen_timestamp, offline=True)
        return None
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.first_seen < other.first_seen
    
    @classmethod
    def from_db(cls, row: Row):
        id = row['id']
        context = row.context()
        bus = context.find_bus(row['vehicle_id'])
        first_seen = Date.parse(row['first_seen'], context.timezone)
        if 'first_record_id' in row:
            row.values['first_record_allocation_id'] = id
            row.values['first_record_agency_id'] = context.agency_id
            row.values['first_record_vehicle_id'] = bus.id
            row.values['first_record_system_id'] = context.system_id
            first_record = row.obj('first_record', Record.from_db)
        else:
            first_record = None
        last_seen = Date.parse(row['last_seen'], context.timezone)
        if 'last_record_id' in row:
            row.values['last_record_allocation_id'] = id
            row.values['last_record_agency_id'] = context.agency_id
            row.values['last_record_vehicle_id'] = bus.id
            row.values['last_record_system_id'] = context.system_id
            last_record = row.obj('last_record', Record.from_db)
        else:
            last_record = None
        active = row['active'] == 1
        last_lat = row['last_lat']
        last_lon = row['last_lon']
        last_stop_id = row['last_stop_id']
        last_stop_number = row['last_stop_number']
        last_stop_name = row['last_stop_name']
        last_seen_timestamp = Timestamp.parse(row['last_seen_timestamp'], context.timezone)
        return cls(id, context, bus, first_seen, first_record, last_seen, last_record, active, last_lat, last_lon, last_stop_id, last_stop_number, last_stop_name, last_seen_timestamp)
