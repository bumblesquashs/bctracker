
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass

from models.bus import Bus
from models.context import Context
from models.date import Date
from models.record import Record
from models.row import Row

@dataclass(slots=True)
class Overview:
    '''An overview of a bus' history'''
    
    bus: Bus
    first_seen_date: Date
    first_seen_system: System
    first_record: Record | None
    last_seen_date: Date
    last_seen_system: System
    last_record: Record | None
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns an overview initialized from the given database row'''
        context = Context.find(agency_id='bc-transit')
        bus = context.find_bus(row['bus_number'])
        first_seen_context = row.context('first_seen_system_id')
        first_seen_date = Date.parse(row['first_seen_date'], first_seen_context.timezone)
        first_record = row.obj('first_record', Record.from_db)
        last_seen_context = row.context('last_seen_system_id')
        last_seen_date = Date.parse(row['last_seen_date'], last_seen_context.timezone)
        last_record = row.obj('last_record', Record.from_db)
        return cls(bus, first_seen_date, first_seen_context.system, first_record, last_seen_date, last_seen_context.system, last_record)
    
    @property
    def first_seen_context(self):
        '''The first seen context for this overview'''
        return self.first_seen_system.context
    
    @property
    def last_seen_context(self):
        '''The last seen context for this overview'''
        return self.last_seen_system.context
