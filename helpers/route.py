
from models.route import Route

import database

def create(system, agency, row):
    '''Inserts a new route into the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    if 'route_color' in row and row['route_color'] != '' and (not system.colour_routes or row['route_color'] != '000000'):
        colour = row['route_color']
    else:
        colour = None
    if 'route_text_color' in row and row['route_text_color'] != '':
        text_colour = row['route_text_color']
    else:
        text_colour = None
    database.insert('route', {
        'system_id': system_id,
        'agency_id': agency_id,
        'route_id': row['route_id'],
        'number': row['route_short_name'],
        'name': row['route_long_name'],
        'colour': colour,
        'text_colour': text_colour
    })

def find(system, agency, route_id):
    '''Returns the route with the given route ID'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    routes = database.select('route',
        columns={
            'route.system_id': 'route_system_id',
            'route.agency_id': 'route_agency_id',
            'route.route_id': 'route_id',
            'route.number': 'route_number',
            'route.name': 'route_name',
            'route.colour': 'route_colour',
            'route.text_colour': 'route_text_colour'
        },
        filters={
            'route.system_id': system_id,
            'route.agency_id': agency_id,
            'route.route_id': route_id
        },
        limit=1,
        initializer=Route.from_db
    )
    if len(routes) == 0:
        return None
    return routes[0]

def find_all(system, agency, limit=None):
    '''Returns all routes'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    return database.select('route',
        columns={
            'route.system_id': 'route_system_id',
            'route.agency_id': 'route_agency_id',
            'route.route_id': 'route_id',
            'route.number': 'route_number',
            'route.name': 'route_name',
            'route.colour': 'route_colour',
            'route.text_colour': 'route_text_colour'
        },
        filters={
            'route.system_id': system_id,
            'route.agency_id': agency_id
        },
        limit=limit,
        initializer=Route.from_db
    )

def delete_all(system, agency):
    '''Deletes all routes from the database'''
    system_id = getattr(system, 'id', system)
    agency_id = getattr(agency, 'id', agency)
    database.delete('route', {
        'system_id': system_id,
        'agency_id': agency_id
    })
