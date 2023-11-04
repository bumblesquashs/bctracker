
import helpers.system

class Point:
    '''The coordinates and sequence number of a single point in a line'''
    
    __slots__ = ('system', 'shape_id', 'sequence', 'lat', 'lon')
    
    @classmethod
    def from_csv(cls, row, system):
        '''Returns a point initialized from the given CSV row'''
        shape_id = row['shape_id']
        sequence = int(row['shape_pt_sequence'])
        lat = float(row['shape_pt_lat'])
        lon = float(row['shape_pt_lon'])
        return cls(system, shape_id, sequence, lat, lon)
    
    @classmethod
    def from_db(cls, row, prefix='point'):
        '''Returns a point initialized from the given database row'''
        system = helpers.system.find(row[f'{prefix}_system_id'])
        shape_id = row[f'{prefix}_shape_id']
        sequence = row[f'{prefix}_sequence']
        lat = row[f'{prefix}_lat']
        lon = row[f'{prefix}_lon']
        return cls(system, shape_id, sequence, lat, lon)
    
    def __init__(self, system, shape_id, sequence, lat, lon):
        self.system = system
        self.shape_id = shape_id
        self.sequence = sequence
        self.lat = lat
        self.lon = lon
    
    def __eq__(self, other):
        return self.sequence == other.sequence
    
    def __lt__(self, other):
        return self.sequence < other.sequence
    
    @property
    def json(self):
        '''Returns a representation of this point in JSON-compatible format'''
        return {
            'lat': self.lat,
            'lon': self.lon,
        }
