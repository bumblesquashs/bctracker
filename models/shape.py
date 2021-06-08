
class Shape:
    def __init__(self, system, shape_id):
        self.system = system
        self.shape_id = shape_id
        self.points = []

    def add_point(self, lat, lon, sequence):
        self.points.append(ShapePoint(lat, lon, sequence))

class ShapePoint:
    def __init__(self, lat, lon, sequence):
        self.lat = lat
        self.lon = lon
        self.sequence = sequence
    
    def __eq__(self, other):
        return self.sequence == other.sequence
    
    def __lt__(self, other):
        return self.sequence < other.sequence
