
from dataclasses import dataclass

from models.row import Row

@dataclass(slots=True)
class Area:
    '''A geographic area defined by min/max latitudes and longitudes'''
    
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns an area initialized from the given database row'''
        area = cls(**row.values)
        if area.min_lat is None and area.max_lat is None and area.min_lon is None and area.max_lon is None:
            return None
        return area
    
    @classmethod
    def calculate(cls, lats: list[float], lons: list[float]):
        '''Returns the area of the given lats and lons'''
        return cls(min(lats), max(lats), min(lons), max(lons))
