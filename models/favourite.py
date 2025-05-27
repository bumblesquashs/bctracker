
from dataclasses import dataclass

from di import di

from models.bus import Bus
from models.context import Context
from models.route import Route
from models.stop import Stop

from repositories import RouteRepository, StopRepository

@dataclass(slots=True)
class Favourite:
    '''A vehicle, route, or stop selected by a user to have quick access to'''
    
    type: str
    value: Bus | Route | Stop
    
    @classmethod
    def parse(cls, string, **kwargs):
        '''Returns a favourite parsed from the given string, or None if parsing fails'''
        parts = string.split(':')
        type = parts[0]
        if type == 'vehicle':
            context = Context.find(agency_id=parts[1])
            value = Bus.find(context, int(parts[2]))
        elif type == 'route':
            route_repository = kwargs.get('route_repository') or di[RouteRepository]
            context = Context.find(system_id=parts[1])
            if context.prefer_route_id:
                value = route_repository.find(context, route_id=parts[2])
            else:
                value = route_repository.find(context, number=parts[2])
        elif type == 'stop':
            stop_repository = kwargs.get('stop_repository') or di[StopRepository]
            context = Context.find(system_id=parts[1])
            if context.prefer_stop_id:
                value = stop_repository.find(context, stop_id=parts[2])
            else:
                value = stop_repository.find(context, number=parts[2])
        else:
            value = None
        if value:
            return cls(type, value)
        return None
    
    def __str__(self):
        if self.type == 'vehicle':
            source = self.value.context.agency_id
            number = str(self.value.number)
        elif self.type == 'route':
            source = self.value.context.system_id
            if self.value.context.prefer_route_id:
                number = self.value.id
            else:
                number = self.value.number
        elif self.type == 'stop':
            source = self.value.context.system_id
            if self.value.context.prefer_stop_id:
                number = self.value.id
            else:
                number = self.value.number
        else:
            source = ''
            number = ''
        return ':'.join([self.type, source, number])
    
    def __hash__(self):
        return hash((self.type, self.value))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __lt__(self, other):
        if self.type == other.type:
            return self.value < other.value
        return self.type < other.type

@dataclass(slots=True)
class FavouriteSet:
    '''A set of favourites selected by a user'''
    
    favourites: set[Favourite]
    
    @classmethod
    def parse(cls, string):
        '''Returns a set of non-null favourites parsed from the given string'''
        parts = string.split(',')
        favourites = [Favourite.parse(p) for p in parts if p != '']
        return cls({f for f in favourites if f})
    
    @property
    def is_full(self):
        '''Checks if the set has the maximum number of favourites'''
        return len(self.favourites) >= 20
    
    def __str__(self):
        return ','.join([str(f) for f in self.favourites])
    
    def __bool__(self):
        return bool(self.favourites)
    
    def __contains__(self, favourite):
        return favourite in self.favourites
    
    def __iter__(self):
        for favourite in sorted(self.favourites):
            yield favourite
    
    def adding(self, favourite):
        '''Returns a copy of this set with the given favourite added'''
        if self.is_full:
            return self
        favourites = self.favourites.copy()
        favourites.add(favourite)
        return FavouriteSet(favourites)
    
    def removing(self, favourite):
        '''Returns a copy of this set with the given favourite removed'''
        favourites = self.favourites.copy()
        if favourite in favourites:
            favourites.remove(favourite)
        return FavouriteSet(favourites)
