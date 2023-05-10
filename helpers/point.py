
from models.point import Point

import database

def create(point):
    database.insert('point', {
        'system_id': point.system.id,
        'shape_id': point.shape_id,
        'sequence': point.sequence,
        'lat': point.lat,
        'lon': point.lon
    })

def find_all(system_id, shape_id=None):
    rows = database.select('point',
        columns={
            'point.system_id': 'point_system_id',
            'point.shape_id': 'point_shape_id',
            'point.sequence': 'point_sequence',
            'point.lat': 'point_lat',
            'point.lon': 'point_lon'
        },
        filters={
            'point.system_id': system_id,
            'point.shape_id': shape_id
        },
        order_by='point.sequence ASC')
    return [Point.from_db(row) for row in rows]

def delete_all(system_id):
    database.delete('point', {
        'point.system_id': system_id
    })
