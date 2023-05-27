
from models.position import Position

import database

def create(position):
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
    return [Position.from_db(row) for row in rows]

def delete_all(system_id):
    database.delete('position', {
        'position.system_id': system_id
    })
