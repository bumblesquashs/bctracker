
from database import Database

from models.route import Route

from repositories import RouteRepository

class SQLRouteRepository(RouteRepository):
    
    __slots__ = (
        'database'
    )
    
    def __init__(self, database: Database):
        self.database = database
    
    def create(self, system, row):
        '''Inserts a new route into the database'''
        system_id = getattr(system, 'id', system)
        try:
            colour = row['route_color']
            if colour == '':
                raise ValueError('Colour must not be empty')
            if colour == system.colour_routes:
                raise ValueError('Colour must be auto-generated')
        except (KeyError, ValueError):
            colour = None
        try:
            text_colour = row['route_text_color']
            if text_colour == '':
                raise ValueError('Text colour must not be empty')
        except (KeyError, ValueError):
            text_colour = None
        route_id = row['route_id']
        number = row['route_short_name']
        if not number:
            number = route_id
        self.database.insert('route', {
            'system_id': system_id,
            'route_id': route_id,
            'number': number,
            'name': row['route_long_name'],
            'colour': colour,
            'text_colour': text_colour
        })
    
    def find(self, system, route_id=None, number=None):
        '''Returns the route with the given system and route ID'''
        system_id = getattr(system, 'id', system)
        routes = self.database.select('route',
            columns={
                'route.system_id': 'route_system_id',
                'route.route_id': 'route_id',
                'route.number': 'route_number',
                'route.name': 'route_name',
                'route.colour': 'route_colour',
                'route.text_colour': 'route_text_colour'
            },
            filters={
                'route.system_id': system_id,
                'route.route_id': route_id,
                'route.number': number
            },
            limit=1,
            initializer=Route.from_db
        )
        try:
            return routes[0]
        except IndexError:
            return None
    
    def find_all(self, system, limit=None):
        '''Returns all routes that match the given system'''
        system_id = getattr(system, 'id', system)
        return self.database.select('route',
            columns={
                'route.system_id': 'route_system_id',
                'route.route_id': 'route_id',
                'route.number': 'route_number',
                'route.name': 'route_name',
                'route.colour': 'route_colour',
                'route.text_colour': 'route_text_colour'
            },
            filters={
                'route.system_id': system_id
            },
            limit=limit,
            initializer=Route.from_db
        )
    
    def delete_all(self, system):
        '''Deletes all routes for the given system from the database'''
        system_id = getattr(system, 'id', system)
        self.database.delete('route', {
            'system_id': system_id
        })
