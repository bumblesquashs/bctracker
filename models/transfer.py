
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass

from models.bus import Bus
from models.context import Context
from models.date import Date
from models.row import Row

@dataclass(slots=True)
class Transfer:
    '''Information about a bus moving from one system to another system'''
    
    id: int
    bus: Bus
    date: Date
    old_system: System
    new_system: System
    
    @property
    def old_context(self):
        '''The old context for this transfer'''
        return self.old_system.context
    
    @property
    def new_context(self):
        '''The new context for this transfer'''
        return self.new_system.context
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a transfer initialized from the given database row'''
        id = row['id']
        context = Context.find(agency_id='bc-transit')
        bus = Bus.find(context, row['bus_number'])
        old_context = row.context('old_system_id')
        new_context = row.context('new_system_id')
        date = Date.parse(row['date'], new_context.timezone)
        return cls(id, bus, date, old_context.system, new_context.system)
