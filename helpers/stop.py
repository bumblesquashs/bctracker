
from models.stop import Stop

import database

def create(system, agency, row):
    '''Inserts a new stop into the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    database.insert('stop', {
        'system_id': system_id,
        'agency_id': agency_id,
        'stop_id': row['stop_id'],
        'number': row['stop_code'],
        'name': row['stop_name'],
        'lat': float(row['stop_lat']),
        'lon': float(row['stop_lon'])
    })

def find(system, agency, stop_id):
    '''Returns the stop with the given ID'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    stops = database.select('stop',
        columns={
            'stop.system_id': 'stop_system_id',
            'stop.agency_id': 'stop_agency_id',
            'stop.stop_id': 'stop_id',
            'stop.number': 'stop_number',
            'stop.name': 'stop_name',
            'stop.lat': 'stop_lat',
            'stop.lon': 'stop_lon'
        },
        filters={
            'stop.system_id': system_id,
            'stop.agency_id': agency_id,
            'stop.stop_id': stop_id
        },
        limit=1,
        initializer=Stop.from_db
    )
    if len(stops) == 0:
        return None
    return stops[0]

def find_all(system, agency, limit=None):
    '''Returns all stops'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    return database.select('stop',
        columns={
            'stop.system_id': 'stop_system_id',
            'stop.agency_id': 'stop_agency_id',
            'stop.stop_id': 'stop_id',
            'stop.number': 'stop_number',
            'stop.name': 'stop_name',
            'stop.lat': 'stop_lat',
            'stop.lon': 'stop_lon'
        },
        filters={
            'stop.system_id': system_id,
            'stop.agency_id': agency_id
        },
        limit=limit,
        initializer=Stop.from_db
    )

def delete_all(system, agency):
    '''Deletes all stops from the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    database.delete('stop', {
        'system_id': system_id,
        'agency_id': agency_id
    })
