
class Shape:
    '''A list of sequential points that form a line on a map'''
    __slots__ = ('system', 'id', 'points')
    
    def __init__(self, system, shape_id):
        self.system = system
        self.id = shape_id
        self.points = []
    
    def add_point(self, lat, lon, sequence):
        self.points.append(ShapePoint(lat, lon, sequence))

class ShapePoint:
    '''The coordinates and sequence number of a single point in a shape'''
    __slots__ = ('lat', 'lon', 'sequence')
    
    def __init__(self, lat, lon, sequence):
        self.lat = lat
        self.lon = lon
        self.sequence = sequence
    
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
