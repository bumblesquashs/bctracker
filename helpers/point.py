
from models.point import Point

import database

def create(system, agency, row):
    '''Inserts a new point into the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    database.insert('point', {
        'system_id': system_id,
        'agency_id': agency_id,
        'shape_id': row['shape_id'],
        'sequence': int(row['shape_pt_sequence']),
        'lat': float(row['shape_pt_lat']),
        'lon': float(row['shape_pt_lon'])
    })

def find_all(system, agency, shape=None):
    '''Returns all points that match the given shape'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    shape_id = getattr(shape, 'id', shape)
    return database.select('point',
        columns={
            'point.system_id': 'point_system_id',
            'point.agency_id': 'point_agency_id',
            'point.shape_id': 'point_shape_id',
            'point.sequence': 'point_sequence',
            'point.lat': 'point_lat',
            'point.lon': 'point_lon'
        },
        filters={
            'point.system_id': system_id,
            'point.agency_id': agency_id,
            'point.shape_id': shape_id
        },
        order_by='point.sequence ASC',
        initializer=Point.from_db
    )

def delete_all(system, agency):
    '''Deletes all points from the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    database.delete('point', {
        'point.system_id': system_id,
        'point.agency_id': agency_id
    })
