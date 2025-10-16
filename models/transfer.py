
from dataclasses import dataclass

from models.context import Context
from models.date import Date
from models.row import Row
from models.vehicle import Vehicle

@dataclass(slots=True)
class Transfer:
    '''Information about a vehicle moving from one system to another system'''
    
    id: int
    date: Date
    old_allocation_id: int
    old_context: Context
    old_vehicle: Vehicle
    new_allocation_id: int
    new_context: Context
    new_vehicle: Vehicle
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a transfer initialized from the given database row'''
        id = row['id']
        old_allocation_id = row['old_allocation_id']
        old_context = row.context('old_allocation_agency_id', 'old_allocation_system_id')
        old_vehicle = old_context.find_vehicle(row['old_allocation_vehicle_id'])
        new_allocation_id = row['new_allocation_id']
        new_context = row.context('new_allocation_agency_id', 'new_allocation_system_id')
        new_vehicle = new_context.find_vehicle(row['new_allocation_vehicle_id'])
        date = Date.parse(row['date'], new_context.timezone)
        return cls(id, date, old_allocation_id, old_context, old_vehicle, new_allocation_id, new_context, new_vehicle)
