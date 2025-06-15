
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.block import Block
    from models.route import Route
    from models.stop import Stop

from dataclasses import dataclass

@dataclass(slots=True)
class Match:
    '''A search result with a value indicating how closely it matches the query'''
    
    name: str
    description: str
    icon: str
    path: str
    value: int
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        if self.value == other.value:
            return self.name < other.name
        return self.value > other.value
    
    def get_json(self, context, get_url):
        '''Returns a representation of this match in JSON-compatible format'''
        return {
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'url': get_url(context, self.path)
        }
    
    @classmethod
    def block(cls, block: Block, query: str):
        '''Returns a match for this block with the given query'''
        id = block.id
        value = 0
        if query in id:
            value += (len(query) / len(id)) * 100
            if id.startswith(query):
                value += len(query)
        return Match(f'Block {id}', f'{block.get_start_time()} - {block.get_end_time()}', 'block', f'blocks/{block.url_id}', value)
    
    @classmethod
    def route(cls, route: Route, query: str):
        '''Returns a match for this route with the given query'''
        number = route.number.lower()
        name = route.name.lower()
        value = 0
        if query in number:
            value += (len(query) / len(number)) * 100
            if number.startswith(query):
                value += len(query)
        elif query in name:
            value += (len(query) / len(name)) * 100
            if name.startswith(query):
                value += len(query)
        return cls(f'Route {route.number}', route.name, 'route', f'routes/{route.url_id}', value)
    
    @classmethod
    def stop(cls, stop: Stop, query: str):
        '''Returns a match for this stop with the given query'''
        number = stop.number.lower()
        name = stop.name.lower()
        value = 0
        if query in number:
            value += (len(query) / len(number)) * 100
            if number.startswith(query):
                value += len(query)
        elif query in name:
            value += (len(query) / len(name)) * 100
            if name.startswith(query):
                value += len(query)
            if value > 20:
                value -= 20
            else:
                value = 1
        return cls(f'Stop {stop.number}', stop.name, 'stop', f'stops/{stop.url_id}', value)
