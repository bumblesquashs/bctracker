
import helpers.agency
import helpers.system

class Point:
    '''The coordinates and sequence number of a single point in a line'''
    
    __slots__ = (
        'system',
        'agency',
        'shape_id',
        'sequence',
        'lat',
        'lon'
    )
    
    @classmethod
    def from_db(cls, row, prefix='point'):
        '''Returns a point initialized from the given database row'''
        system = helpers.system.find(row[f'{prefix}_system_id'])
        agency = helpers.agency.find(row[f'{prefix}_agency_id'])
        shape_id = row[f'{prefix}_shape_id']
        sequence = row[f'{prefix}_sequence']
        lat = row[f'{prefix}_lat']
        lon = row[f'{prefix}_lon']
        return cls(system, agency, shape_id, sequence, lat, lon)
    
    def __init__(self, system, agency, shape_id, sequence, lat, lon):
        self.system = system
        self.agency = agency
        self.shape_id = shape_id
        self.sequence = sequence
        self.lat = lat
        self.lon = lon
    
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
