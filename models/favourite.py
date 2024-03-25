
import helpers.agency
import helpers.order
import helpers.route
import helpers.stop
import helpers.system

from models.bus import Bus

import utils

class Favourite:
    
    __slots__ = (
        'source',
        'type',
        'number',
        'key'
    )
    
    @classmethod
    def parse(cls, string):
        parts = string.split(':')
        source = parts[0]
        type = parts[1]
        number = parts[2]
        return cls(source, type, number)
    
    @property
    def value(self):
        if self.type == 'vehicle':
            return Bus.find(self.source, int(self.number))
        if self.type == 'route':
            return helpers.route.find(self.source, number=self.number)
        if self.type == 'stop':
            return helpers.stop.find(self.source, number=self.number)
        return None
    
    @property
    def agency(self):
        if self.type == 'vehicle':
            return helpers.agency.find(self.source)
        return None
    
    @property
    def system(self):
        if self.type == 'route' or self.type == 'stop':
            return helpers.system.find(self.source)
        return None
    
    def __init__(self, source, type, number):
        self.source = source
        self.type = type
        self.number = number
        
        self.key = utils.key(number)
    
    def __str__(self):
        return ':'.join([self.source, self.type, self.number])
    
    def __hash__(self):
        return hash((self.source, self.type, self.number))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __lt__(self, other):
        if self.type == other.type:
            if self.key == other.key:
                return self.source < other.source
            return self.key < other.key
        return self.type < other.type

class FavouriteSet:
    
    __slots__ = (
        'favourites'
    )
    
    @classmethod
    def parse(cls, string):
        parts = string.split(',')
        favourites = [Favourite.parse(p) for p in parts if p != '']
        return cls(favourites)
    
    @property
    def is_full(self):
        return len(self.favourites) >= 10
    
    def __init__(self, favourites):
        self.favourites = set(favourites)
    
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
        if self.is_full:
            return self
        favourites = self.favourites.copy()
        favourites.add(favourite)
        return FavouriteSet(favourites)
    
    def removing(self, favourite):
        favourites = self.favourites.copy()
        if favourite in favourites:
            favourites.remove(favourite)
        return FavouriteSet(favourites)
