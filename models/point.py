
from dataclasses import dataclass

from models.context import Context

@dataclass(slots=True)
class Point:
    '''The coordinates and sequence number of a single point in a line'''
    
    context: Context
    shape_id: str
    sequence: int
    lat: float
    lon: float
    
    @classmethod
    def from_db(cls, row, prefix='point'):
        '''Returns a point initialized from the given database row'''
        context = Context.find(system_id=row[f'{prefix}_system_id'])
        shape_id = row[f'{prefix}_shape_id']
        sequence = row[f'{prefix}_sequence']
        lat = row[f'{prefix}_lat']
        lon = row[f'{prefix}_lon']
        return cls(context, shape_id, sequence, lat, lon)
    
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
