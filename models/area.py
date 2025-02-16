
class Area:
    '''A geographic area defined by min/max latitudes and longitudes'''
    
    __slots__ = (
        'min_lat',
        'max_lat',
        'min_lon',
        'max_lon'
    )
    
    @classmethod
    def from_db(cls, row):
        '''Returns an area initialized from the given database row'''
        area = cls(**row)
        if area.min_lat is None and area.max_lat is None and area.min_lon is None and area.max_lon is None:
            return None
        return area
    
    @classmethod
    def calculate(cls, lats, lons):
        '''Returns the area of the given lats and lons'''
        return cls(min(lats), max(lats), min(lons), max(lons))
    
    def __init__(self, min_lat, max_lat, min_lon, max_lon):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
    
    def __eq__(self, other):
        return self.min_lat == other.min_lat and self.max_lat == other.max_lat and self.min_lon == other.min_lon and self.max_lon == other.max_lon
