
import math

from enum import Enum

class Direction(Enum):
    '''A basic description of the path a trip follows'''
    
    CIRCULAR = 'Circular'
    SOUTHBOUND = 'Southbound'
    NORTHBOUND = 'Northbound'
    WESTBOUND = 'Westbound'
    EASTBOUND = 'Eastbound'
    UNKNOWN = 'Unknown'
    
    @classmethod
    def calculate(cls, p1, p2):
        lat_diff = p2.lat - p1.lat
        lon_diff = p2.lon - p1.lon
        if abs(lat_diff) <= 0.001 and abs(lon_diff) <= 0.001:
            return cls.CIRCULAR
        angle = math.degrees(math.atan2(lat_diff, lon_diff))
        if angle < 45:
            return cls.EASTBOUND
        if angle < 135:
            return cls.NORTHBOUND
        if angle < 225:
            return cls.WESTBOUND
        if angle < 315:
            return cls.SOUTHBOUND
        if angle < 360:
            return cls.EASTBOUND
        return cls.UNKNOWN
    
    def __str__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value
