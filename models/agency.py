
from constants import *

class Agency:
    '''A company or entity that runs transit'''
    
    __slots__ = (
        'id',
        'name',
        'website',
        'gtfs_url',
        'realtime_url',
        'enabled',
        'prefix_headsigns',
        'accurate_seconds',
        'prefer_route_id',
        'prefer_stop_id',
        'show_stop_number',
        'vehicle_name_length',
        'distance_scale'
    )
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS is enabled for this agency'''
        return self.enabled and self.gtfs_url
    
    @property
    def realtime_enabled(self):
        '''Checks if realtime is enabled for this agency'''
        return self.enabled and self.realtime_url
    
    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.website = kwargs.get('website')
        self.gtfs_url = kwargs.get('gtfs_url')
        self.realtime_url = kwargs.get('realtime_url')
        self.enabled = kwargs.get('enabled', True)
        self.prefix_headsigns = kwargs.get('prefix_headsigns', DEFAULT_PREFIX_HEADSIGNS)
        self.accurate_seconds = kwargs.get('accurate_seconds', DEFAULT_ACCURATE_SECONDS)
        self.prefer_route_id = kwargs.get('prefer_route_id', DEFAULT_PREFER_ROUTE_ID)
        self.prefer_stop_id = kwargs.get('prefer_stop_id', DEFAULT_PREFER_STOP_ID)
        self.show_stop_number = kwargs.get('show_stop_number', DEFAULT_SHOW_STOP_NUMBER)
        self.vehicle_name_length = kwargs.get('vehicle_name_length', DEFAULT_VEHICLE_NAME_LENGTH)
        self.distance_scale = kwargs.get('distance_scale', DEFAULT_DISTANCE_SCALE)
    
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
