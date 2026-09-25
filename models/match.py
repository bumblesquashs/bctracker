
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.block import Block
    from models.route import Route
    from models.stop import Stop
    from models.vehicle import Vehicle

from dataclasses import dataclass

from models.context import Context

@dataclass(slots=True)
class Match:
    '''A search result with a value indicating how closely it matches the query'''
    
    context: Context
    type: str
    entity: Block | Route | Stop | Vehicle
    value: int
    key: tuple
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        if self.value == other.value:
            return self.key < other.key
        return self.value > other.value
    
    def get_json(self):
        '''Returns a representation of this match in JSON-compatible format'''
        match self.type:
            case 'block':
                data = {
                    'id': self.entity.id,
                    'routes': [r.get_json() for r in self.entity.get_routes()],
                }
            case 'route':
                data = self.entity.get_json()
            case 'stop':
                data = self.entity.get_json()
            case 'vehicle':
                decoration = self.entity.find_decoration()
                data = {
                    'id': self.entity.id,
                    'name': self.entity.name,
                    'year_model': self.entity.year_model,
                    'title_prefix': self.entity.model.type.title_prefix if self.entity.model else None,
                    'icon': f'model/type/{self.entity.model.type.image_name}' if self.entity.model else 'ghost',
                    'decoration': decoration.text if decoration else None,
                }
        return {
            'agency_id': self.context.agency_id,
            'system_name': str(self.context),
            'type': self.type,
            'data': data,
            'url': self.entity.url(),
        }
    
    @classmethod
    def block(cls, block: Block, value: int):
        return cls(
            context=block.context,
            type='block',
            entity=block,
            value=value,
            key=((block.id,),),
        )
    
    @classmethod
    def route(cls, route: Route, value: int):
        return cls(
            context=route.context,
            type='route',
            entity=route,
            value=value,
            key=(route.key, route.name),
        )
    
    @classmethod
    def stop(cls, stop: Stop, value: int):
        return cls(
            context=stop.context,
            type='stop',
            entity=stop,
            value=value,
            key=(stop.key, stop.name),
        )
    
    @classmethod
    def vehicle(cls, vehicle: Vehicle, value: int):
        return cls(
            context=vehicle.context,
            type='vehicle',
            entity=vehicle,
            value=value,
            key=((vehicle.id,),),
        )
