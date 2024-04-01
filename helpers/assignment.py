
from models.assignment import Assignment
from models.date import Date

import database

def create(system, block, bus, date):
    '''Inserts a new assignment into the database'''
    system_id = getattr(system, 'id', system)
    block_id = getattr(block, 'id', block)
    bus_number = getattr(bus, 'number', bus)
    database.insert('assignment', {
        'system_id': system_id,
        'block_id': block_id,
        'bus_number': bus_number,
        'date': date.format_db()
    })

def find(system, block):
    '''Returns the assignment for the given system and block'''
    system_id = getattr(system, 'id', system)
    block_id = getattr(block, 'id', block)
    try:
        date = Date.today(system.timezone)
    except:
        date = Date.today()
    assignments = database.select('assignment',
        columns={
            'assignment.system_id': 'assignment_system_id',
            'assignment.block_id': 'assignment_block_id',
            'assignment.bus_number': 'assignment_bus_number',
            'assignment.date': 'assignment_date'
        },
        filters={
            'assignment.system_id': system_id,
            'assignment.block_id': block_id,
            'assignment.date': date.format_db()
        },
        initializer=Assignment.from_db
    )
    try:
        return assignments[0]
    except IndexError:
        return None

def find_all(system=None, block=None, bus=None, trip=None, route=None, stop=None):
    '''Returns all assignments for the given block, bus, trip, route, and stop'''
    system_id = getattr(system, 'id', system)
    block_id = getattr(block, 'id', block)
    bus_number = getattr(bus, 'number', bus)
    trip_id = getattr(trip, 'id', trip)
    route_id = getattr(route, 'id', route)
    stop_id = getattr(stop, 'id', stop)
    try:
        date = Date.today(system.timezone)
    except AttributeError:
        date = Date.today()
    joins = {}
    filters = {
        'assignment.system_id': system_id,
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
    assignments = database.select('assignment',
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

def delete_all(system=None, block=None, bus=None):
    '''Deletes all assignments from the database'''
    system_id = getattr(system, 'id', system)
    block_id = getattr(block, 'id', block)
    bus_number = getattr(bus, 'number', bus)
    database.delete('assignment', {
        'system_id': system_id,
        'block_id': block_id,
        'bus_number': bus_number
    })
