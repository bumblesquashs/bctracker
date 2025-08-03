
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.date import Date
from models.transfer import Transfer

@dataclass(slots=True)
class TransferRepository:
    
    database: Database
    
    def create(self, date: Date, old_allocation_id: int, new_allocation_id: int):
        '''Inserts a new transfer into the database'''
        self.database.insert('transfer', {
            'date': date.format_db(),
            'old_allocation_id': old_allocation_id,
            'new_allocation_id': new_allocation_id
        })
    
    def find_all(self, old_context: Context, new_context: Context) -> list[Transfer]:
        '''Returns all transfers that match the given system'''
        return self.database.select('transfer',
            columns={
                'transfer.transfer_id': 'id',
                'transfer.date': 'date',
                'transfer.old_allocation_id': 'old_allocation_id',
                'old_allocation.agency_id': 'old_allocation_agency_id',
                'old_allocation.vehicle_id': 'old_allocation_vehicle_id',
                'old_allocation.system_id': 'old_allocation_system_id',
                'transfer.new_allocation_id': 'new_allocation_id',
                'new_allocation.agency_id': 'new_allocation_agency_id',
                'new_allocation.vehicle_id': 'new_allocation_vehicle_id',
                'new_allocation.system_id': 'new_allocation_system_id'
            },
            filters={
                'old_allocation.agency_id': old_context.agency_id,
                'old_allocation.system_id': old_context.system_id,
                'new_allocation.agency_id': new_context.agency_id,
                'new_allocation.system_id': new_context.system_id,
            },
            joins={
                'allocation old_allocation': {
                    'old_allocation.allocation_id': 'transfer.old_allocation_id'
                },
                'allocation new_allocation': {
                    'new_allocation.allocation_id': 'transfer.new_allocation_id'
                }
            },
            order_by={
                'transfer.date': 'DESC',
                'transfer.transfer_id': 'DESC'
            },
            initializer=Transfer.from_db
        )
    
    def find_all_by_bus(self, context: Context, vehicle_id: str) -> list[Transfer]:
        return self.database.select(
            table='transfer',
            columns={
                'transfer.transfer_id': 'id',
                'transfer.date': 'date',
                'transfer.old_allocation_id': 'old_allocation_id',
                'old_allocation.agency_id': 'old_allocation_agency_id',
                'old_allocation.vehicle_id': 'old_allocation_vehicle_id',
                'old_allocation.system_id': 'old_allocation_system_id',
                'transfer.new_allocation_id': 'new_allocation_id',
                'new_allocation.agency_id': 'new_allocation_agency_id',
                'new_allocation.vehicle_id': 'new_allocation_vehicle_id',
                'new_allocation.system_id': 'new_allocation_system_id'
            },
            filters={
                'old_allocation.agency_id': context.agency_id,
                'old_allocation.vehicle_id': vehicle_id,
                'new_allocation.agency_id': context.agency_id,
                'new_allocation.vehicle_id': vehicle_id
            },
            joins={
                'allocation old_allocation': {
                    'old_allocation.allocation_id': 'transfer.old_allocation_id'
                },
                'allocation new_allocation': {
                    'new_allocation.allocation_id': 'transfer.new_allocation_id'
                }
            },
            order_by={
                'transfer.date': 'DESC',
                'transfer.transfer_id': 'DESC'
            },
            initializer=Transfer.from_db
        )
