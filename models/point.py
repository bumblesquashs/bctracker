
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass

from models.row import Row

@dataclass(slots=True)
class Point:
    '''The coordinates and sequence number of a single point in a line'''
    
    system: System
    shape_id: str
    sequence: int
    lat: float
    lon: float
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a point initialized from the given database row'''
        context = row.context()
        shape_id = row['shape_id']
        sequence = row['sequence']
        lat = row['lat']
        lon = row['lon']
        return cls(context.system, shape_id, sequence, lat, lon)
    
    @property
    def context(self):
        '''The context for this point'''
        return self.system.context
    
    def __eq__(self, other):
        return self.sequence == other.sequence
    
    def __lt__(self, other):
        return self.sequence < other.sequence
    
    def get_json(self):
        '''Returns a representation of this point in JSON-compatible format'''
        return {
            'lat': self.lat,
            'lon': self.lon,
        }
