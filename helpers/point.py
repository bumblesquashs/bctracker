
from models.point import Point

import database

def create(system, row):
    '''Inserts a new point into the database'''
    database.insert('point', {
        'system_id': system.id,
        'shape_id': row['shape_id'],
        'sequence': int(row['shape_pt_sequence']),
        'lat': float(row['shape_pt_lat']),
        'lon': float(row['shape_pt_lon'])
    })

def find_all(system_id, shape_id=None):
    '''Returns all points that match the given system ID and shape ID'''
    return database.select('point',
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
        order_by='point.sequence ASC',
        initializer=Point.from_db
    )

def delete_all(system):
    '''Deletes all points for the given system from the database'''
    database.delete('point', {
        'point.system_id': system.id
    })
