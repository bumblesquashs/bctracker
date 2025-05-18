
from database import Database

from models.assignment import Assignment
from models.context import Context
from models.date import Date

class AssignmentRepository:
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database: Database):
        self.database = database
    
    def create(self, context: Context, block, bus, date):
        '''Inserts a new assignment into the database'''
        block_id = getattr(block, 'id', block)
        bus_number = getattr(bus, 'number', bus)
        self.database.insert('assignment', {
            'system_id': context.system_id,
            'block_id': block_id,
            'bus_number': bus_number,
            'date': date.format_db()
        })
    
    def find(self, context: Context, block):
        '''Returns the assignment for the given context and block'''
        block_id = getattr(block, 'id', block)
        date = Date.today(context.timezone)
        assignments = self.database.select('assignment',
            columns={
                'assignment.system_id': 'assignment_system_id',
                'assignment.block_id': 'assignment_block_id',
                'assignment.bus_number': 'assignment_bus_number',
                'assignment.date': 'assignment_date'
            },
            filters={
                'assignment.system_id': context.system_id,
                'assignment.block_id': block_id,
                'assignment.date': date.format_db()
            },
            initializer=Assignment.from_db
        )
        try:
            return assignments[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context, block=None, bus=None, trip=None, route=None, stop=None):
        '''Returns all assignments for the given block, bus, trip, route, and stop'''
        block_id = getattr(block, 'id', block)
        bus_number = getattr(bus, 'number', bus)
        trip_id = getattr(trip, 'id', trip)
        route_id = getattr(route, 'id', route)
        stop_id = getattr(stop, 'id', stop)
        date = Date.today(context.timezone)
        joins = {}
        filters = {
            'assignment.system_id': context.system_id,
            'assignment.block_id': block_id,
            'assignment.bus_number': bus_number,
            'assignment.date': date.format_db()
        }
        if trip_id or route_id or stop_id:
            joins['trip'] = {
                'trip.system_id': 'assignment.system_id',
                'trip.block_id': 'assignment.block_id'
            }
            filters['trip.trip_id'] = trip_id
            filters['trip.route_id'] = route_id
            if stop_id:
                joins['departure'] = {
                    'departure.system_id': 'trip.system_id',
                    'departure.trip_id': 'trip.trip_id'
                }
                filters['departure.stop_id'] = stop_id
        assignments = self.database.select('assignment',
            columns={
                'assignment.system_id': 'assignment_system_id',
                'assignment.block_id': 'assignment_block_id',
                'assignment.bus_number': 'assignment_bus_number',
                'assignment.date': 'assignment_date'
            },
            joins=joins,
            filters=filters,
            initializer=Assignment.from_db
        )
        return {a.key: a for a in assignments}
    
    def delete_all(self, context: Context, block=None, bus=None):
        '''Deletes all assignments from the database'''
        block_id = getattr(block, 'id', block)
        bus_number = getattr(bus, 'number', bus)
        self.database.delete('assignment', {
            'system_id': context.system_id,
            'block_id': block_id,
            'bus_number': bus_number
        })
