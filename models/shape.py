
class Shape:
    '''A list of sequential points that form a line on a map'''
    
    __slots__ = ('system', 'id', 'points')
    
    def __init__(self, system, id, points):
        self.system = system
        self.id = id
        self.points = sorted(points)

class ShapePoint:
    '''The coordinates and sequence number of a single point in a shape'''
    
    __slots__ = ('shape_id', 'sequence', 'lat', 'lon')
    
    @classmethod
    def from_csv(cls, row):
        shape_id = row['shape_id']
        sequence = int(row['shape_pt_sequence'])
        lat = float(row['shape_pt_lat'])
        lon = float(row['shape_pt_lon'])
        return cls(shape_id, sequence, lat, lon)
    
    def __init__(self, shape_id, sequence, lat, lon):
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
        return {
            'lon': self.lon,
            'lat': self.lat
        }
