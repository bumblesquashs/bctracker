
from dataclasses import dataclass

from constants import *

@dataclass(slots=True)
class Agency:
    '''A company or entity that runs transit'''
    
    id: str
    name: str
    
    website: str | None = None
    gtfs_url: str | None = None
    realtime_url: str | None = None
    enabled: bool = True
    prefix_headsigns: bool = DEFAULT_PREFIX_HEADSIGNS
    accurate_seconds: bool = DEFAULT_ACCURATE_SECONDS
    prefer_route_id: bool = DEFAULT_PREFER_ROUTE_ID
    prefer_stop_id: bool = DEFAULT_PREFER_STOP_ID
    show_stop_number: bool = DEFAULT_SHOW_STOP_NUMBER
    vehicle_name_length: int | None = DEFAULT_VEHICLE_NAME_LENGTH
    distance_scale: int = DEFAULT_DISTANCE_SCALE
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS is enabled for this agency'''
        return self.enabled and self.gtfs_url
    
    @property
    def realtime_enabled(self):
        '''Checks if realtime is enabled for this agency'''
        return self.enabled and self.realtime_url
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
