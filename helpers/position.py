
from models.position import Position

import database

in_memory_bcf_positions_hack = []

def set_in_memory_bcf_positions_hack(positions):
    global in_memory_bcf_positions_hack
    in_memory_bcf_positions_hack = positions

def create(position):
    '''Inserts a new position into the database'''
    values = {
        'system_id': position.system.id,
        'bus_number': position.bus.number,
        'trip_id': position.trip_id,
        'stop_id': position.stop_id,
        'block_id': position.block_id,
        'route_id': position.route_id,
        'lat': position.lat,
        'lon': position.lon,
        'bearing': position.bearing,
        'speed': position.speed
    }
    if position.adherence is not None:
        values['adherence'] = position.adherence.value
    database.insert('position', values)

def find(bus_number):
    '''Returns the position of the bus with the given number'''
    
    # TODO: REMOVE
    for pos in in_memory_bcf_positions_hack:
        if pos.bus.id == bus_number: # TODO: REMOVE
            return pos # TODO: REMOVE
    
    rows = database.select('position',
        columns={
            'position.system_id': 'position_system_id',
            'position.bus_number': 'position_bus_number',
            'position.trip_id': 'position_trip_id',
            'position.stop_id': 'position_stop_id',
            'position.block_id': 'position_block_id',
            'position.route_id': 'position_route_id',
            'position.lat': 'position_lat',
            'position.lon': 'position_lon',
            'position.bearing': 'position_bearing',
            'position.speed': 'position_speed',
            'position.adherence': 'position_adherence'
        },
        filters={
            'position.bus_number': bus_number
        })
    if len(rows) == 1:
        return Position.from_db(rows[0])
    return None

def find_all(system_id=None, trip_id=None, stop_id=None, block_id=None, route_id=None, has_location=None):
    '''Returns all positions that match the given system, trip, stop, block, and route'''
    filters = {
        'position.system_id': system_id,
        'position.trip_id': trip_id,
        'position.stop_id': stop_id,
        'position.block_id': block_id,
        'position.route_id': route_id
    }
    if has_location is not None:
        if has_location:
            filters['position.lat'] = {
                'IS NOT': None
            }
            filters['position.lon'] = {
                'IS NOT': None
            }
        else:
            filters['position.lat'] = {
                'IS': None
            }
            filters['position.lon'] = {
                'IS': None
            }
    rows = database.select('position',
        columns={
            'position.system_id': 'position_system_id',
            'position.bus_number': 'position_bus_number',
            'position.trip_id': 'position_trip_id',
            'position.stop_id': 'position_stop_id',
            'position.block_id': 'position_block_id',
            'position.route_id': 'position_route_id',
            'position.lat': 'position_lat',
            'position.lon': 'position_lon',
            'position.bearing': 'position_bearing',
            'position.speed': 'position_speed',
            'position.adherence': 'position_adherence'
        },
        filters=filters)
    positions = [Position.from_db(row) for row in rows]
    
    # TODO: REMOVE ALL THIS
    if system_id is None or system_id == 'bc-ferries':
        manual_filtering_hack = in_memory_bcf_positions_hack
        if route_id is not None:
            manual_filtering_hack = [p for p in manual_filtering_hack if p.route.id == route_id]
            
        if trip_id is not None:
            manual_filtering_hack = [p for p in manual_filtering_hack if p.trip.id == trip_id]
            
        # TODO: REMOVE ALL THIS
        positions = positions + manual_filtering_hack
        
    return [p for p in positions if not p.bus.is_test]

def delete_all(system_id=None):
    '''Deletes all positions for the given system from the database'''
    database.delete('position', {
        'position.system_id': system_id
    })
