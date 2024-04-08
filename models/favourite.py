
import helpers.agency
import helpers.route
import helpers.stop
import helpers.system

from models.bus import Bus

class Favourite:
    '''A vehicle, route, or stop selected by a user to have quick access to'''
    
    __slots__ = (
        'type',
        'value'
    )
    
    @classmethod
    def parse(cls, string):
        '''Returns a favourite parsed from the given string, or None if parsing fails'''
        parts = string.split(':')
        type = parts[0]
        if type == 'vehicle':
            value = Bus.find(parts[1], int(parts[2]))
        elif type == 'route':
            value = helpers.route.find(parts[1], number=parts[2])
        elif type == 'stop':
            value = helpers.stop.find(parts[1], number=parts[2])
        else:
            value = None
        if value:
            return cls(type, value)
        return None
    
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        if self.type == 'vehicle':
            source = self.value.order.agency.id
            number = str(self.value.number)
        elif self.type == 'route':
            source = self.value.system.id
            number = self.value.number
        elif self.type == 'stop':
            source = self.value.system.id
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

class FavouriteSet:
    '''A set of favourites selected by a user'''
    
    __slots__ = (
        'favourites'
    )
    
    @classmethod
    def parse(cls, string):
        '''Returns a set of non-null favourites parsed from the given string'''
        parts = string.split(',')
        favourites = [Favourite.parse(p) for p in parts if p != '']
        return cls({f for f in favourites if f})
    
    @property
    def is_full(self):
        '''Checks if the set has the maximum number of favourites'''
        return len(self.favourites) >= 10
    
    def __init__(self, favourites):
        self.favourites = favourites
    
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
