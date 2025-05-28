
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.route import Route

@dataclass(slots=True)
class RouteRepository:
    
    database: Database
    
    def create(self, context: Context, row):
        '''Inserts a new route into the database'''
        try:
            colour = row['route_color']
            if colour == '':
                raise ValueError('Colour must not be empty')
            if colour == context.system.colour_routes:
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
            'system_id': context.system_id,
            'route_id': route_id,
            'number': number,
            'name': row['route_long_name'],
            'colour': colour,
            'text_colour': text_colour
        })
    
    def find(self, context: Context, route_id=None, number=None) -> Route | None:
        '''Returns the route with the given context and route ID'''
        routes = self.database.select('route',
            columns={
                'route.system_id': 'system_id',
                'route.route_id': 'id',
                'route.number': 'number',
                'route.name': 'name',
                'route.colour': 'colour',
                'route.text_colour': 'text_colour'
            },
            filters={
                'route.system_id': context.system_id,
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
    
    def find_all(self, context: Context, limit=None) -> list[Route]:
        '''Returns all routes that match the given context'''
        return self.database.select('route',
            columns={
                'route.system_id': 'system_id',
                'route.route_id': 'id',
                'route.number': 'number',
                'route.name': 'name',
                'route.colour': 'colour',
                'route.text_colour': 'text_colour'
            },
            filters={
                'route.system_id': context.system_id
            },
            limit=limit,
            initializer=Route.from_db
        )
    
    def delete_all(self, context: Context):
        '''Deletes all routes for the given context from the database'''
        self.database.delete('route', {
            'system_id': context.system_id
        })
