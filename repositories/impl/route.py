
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
        try:
            type = int(row['route_type'])
        except (KeyError, ValueError):
            type = None
        try:
            sort_order = int(row['route_sort_order'])
        except (KeyError, ValueError):
            sort_order = None
        route_id = row['route_id']
        number = row['route_short_name']
        if not number:
            try:
                number = context.agency.custom_route_numbers[route_id]
            except KeyError:
                number = route_id
        self.database.insert(
            table='route',
            values={
                'system_id': context.system_id,
                'route_id': route_id,
                'number': number,
                'name': row['route_long_name'],
                'colour': colour,
                'text_colour': text_colour,
                'type': type,
                'sort_order': sort_order
            }
        )
    
    def find(self, context: Context, route_id=None, number=None) -> Route | None:
        '''Returns the route with the given context and route ID'''
        routes = self.database.select(
            table='route',
            columns={
                'route.system_id': 'system_id',
                'route.route_id': 'id',
                'route.number': 'number',
                'route.name': 'name',
                'route.colour': 'colour',
                'route.text_colour': 'text_colour',
                'route.type': 'type',
                'route.sort_order': 'sort_order'
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
        return self.database.select(
            table='route',
            columns={
                'route.system_id': 'system_id',
                'route.route_id': 'id',
                'route.number': 'number',
                'route.name': 'name',
                'route.colour': 'colour',
                'route.text_colour': 'text_colour',
                'route.type': 'type',
                'route.sort_order': 'sort_order'
            },
            filters={
                'route.system_id': context.system_id
            },
            limit=limit,
            initializer=Route.from_db
        )
    
    def delete_all(self, context: Context):
        '''Deletes all routes for the given context from the database'''
        self.database.delete(
            table='route',
            filters={
                'system_id': context.system_id
            }
        )
