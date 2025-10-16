
from dataclasses import dataclass

from database import Database

from models.assignment import Assignment
from models.context import Context
from models.date import Date

@dataclass(slots=True)
class AssignmentRepository:
    
    database: Database
    
    def create(self, block_id: str, allocation_id: int, date: Date):
        '''Inserts a new assignment into the database'''
        self.database.insert(
            table='assignment',
            values={
                'block_id': block_id,
                'allocation_id': allocation_id,
                'date': date.format_db()
            }
        )
    
    def find(self, block_id: str, allocation_id: int, date: Date) -> Assignment | None:
        '''Returns the assignment for the given context and block'''
        assignments = self.database.select(
            table='assignment',
            columns={
                'assignment.block_id': 'block_id',
                'assignment.allocation_id': 'allocation_id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'assignment.date': 'date'
            },
            filters={
                'assignment.block_id': block_id,
                'assignment.allocation_id': allocation_id,
                'assignment.date': date.format_db()
            },
            joins={
                'allocation': {
                    'allocation.allocation_id': 'assignment.allocation_id'
                }
            },
            limit=1,
            initializer=Assignment.from_db
        )
        try:
            return assignments[0]
        except IndexError:
            return None
    
    def find_by_context(self, context: Context, block_id: str) -> Assignment | None:
        assignments = self.database.select(
            table='assignment',
            columns={
                'assignment.block_id': 'block_id',
                'assignment.allocation_id': 'allocation_id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'assignment.date': 'date'
            },
            filters={
                'allocation.agency_id': context.agency_id,
                'allocation.system_id': context.system_id,
                'assignment.block_id': block_id
            },
            joins={
                'allocation': {
                    'allocation.allocation_id': 'assignment.allocation_id'
                }
            },
            limit=1,
            initializer=Assignment.from_db
        )
        try:
            return assignments[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context, block_id: str | None = None, vehicle_id: str | None = None, trip_id: str | None = None, route_id: str | None = None, stop_id: str | None = None) -> list[Assignment]:
        '''Returns all assignments for the given block, vehicle, trip, route, and stop'''
        date = Date.today(context.timezone)
        joins = {
            'allocation': {
                'allocation.allocation_id': 'assignment.allocation_id'
            }
        }
        filters = {
            'allocation.agency_id': context.agency_id,
            'allocation.vehicle_id': vehicle_id,
            'allocation.system_id': context.system_id,
            'assignment.block_id': block_id,
            'assignment.date': date.format_db()
        }
        if trip_id or route_id or stop_id:
            joins['trip'] = {
                # 'trip.agency_id': 'allocation.agency_id',
                'trip.system_id': 'allocation.system_id',
                'trip.block_id': 'assignment.block_id'
            }
            filters['trip.trip_id'] = trip_id
            filters['trip.route_id'] = route_id
            if stop_id:
                joins['departure'] = {
                    # 'departure.agency_id': 'trip.agency_id',
                    'departure.system_id': 'trip.system_id',
                    'departure.trip_id': 'trip.trip_id'
                }
                filters['departure.stop_id'] = stop_id
        assignments = self.database.select(
            table='assignment',
            columns={
                'assignment.block_id': 'block_id',
                'assignment.allocation_id': 'allocation_id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'assignment.date': 'date'
            },
            joins=joins,
            filters=filters,
            initializer=Assignment.from_db
        )
        return assignments
    
    def delete_all(self, block_id: str | None = None, allocation_id: int | None = None):
        '''Deletes all assignments from the database'''
        self.database.delete(
            table='assignment',
            filters={
                'block_id': block_id,
                'allocation_id': allocation_id
            }
        )
