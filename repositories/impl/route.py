
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.match import Match
from models.route import Route

@dataclass(slots=True)
class RouteRepository:
    
    database: Database
    
    def create(self, download_id: int, context: Context, row: dict):
        '''Inserts a new route into the database'''
        try:
            colour = row['route_color']
            if colour == '':
                raise ValueError('Colour must not be empty')
            if colour == context.ignore_route_colour:
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
                'download_id': download_id,
                'route_id': route_id,
                'number': number,
                'name': row['route_long_name'],
                'colour': colour,
                'text_colour': text_colour,
                'type': type,
                'sort_order': sort_order
            }
        )
    
    def find(self, context: Context, route_id: str | None = None, number: str | None = None) -> Route | None:
        '''Returns the route with the given context and route ID'''
        routes = self.database.select(
            table='route',
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'route.route_id': 'route_id',
                'route.number': 'number',
                'route.name': 'name',
                'route.colour': 'colour',
                'route.text_colour': 'text_colour',
                'route.type': 'type',
                'route.sort_order': 'sort_order'
            },
            joins={
                'download': {
                    'download.download_id': 'route.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
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
    
    def find_all(self, context: Context, route_number: str | None = None, limit: int | None = None) -> list[Route]:
        '''Returns all routes that match the given context'''
        return self.database.select(
            table='route',
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'route.route_id': 'route_id',
                'route.number': 'number',
                'route.name': 'name',
                'route.colour': 'colour',
                'route.text_colour': 'text_colour',
                'route.type': 'type',
                'route.sort_order': 'sort_order'
            },
            joins={
                'download': {
                    'download.download_id': 'route.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
                'route.number': route_number
            },
            limit=limit,
            initializer=Route.from_db
        )
    
    def find_matches(self, context: Context, query: str) -> list[Match]:
        routes = self.database.select(
            table='route',
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'route.route_id': 'route_id',
                'route.number': 'number',
                'route.name': 'name',
                'route.colour': 'colour',
                'route.text_colour': 'text_colour',
                'route.type': 'type',
                'route.sort_order': 'sort_order'
            },
            joins={
                'download': {
                    'download.download_id': 'route.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
                'OR': {
                    'route.number': {
                        'LIKE': f'%{query}%'
                    },
                    'route.name': {
                        'LIKE': f'%{query}%'
                    }
                }
            },
            initializer=Route.from_db
        )
        return [r.get_match(query) for r in routes]
    
    def delete_all(self, context: Context):
        '''Deletes all routes for the given context from the database'''
        download_ids = self.database.select(
            table='route',
            columns={
                'route.download_id': 'download_id'
            },
            distinct=True,
            joins={
                'download': {
                    'download.download_id': 'route.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id
            },
            initializer=lambda r: r['download_id']
        )
        if not download_ids:
            return
        if len(download_ids) == 1:
            download_ids = download_ids[0]
        self.database.delete(
            table='route',
            filters={
                'download_id': download_ids
            }
        )
