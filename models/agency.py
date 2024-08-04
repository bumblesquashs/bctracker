
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
        self.prefix_headsigns = kwargs.get('prefix_headsigns', False)
        self.accurate_seconds = kwargs.get('accurate_seconds', True)
        self.vehicle_name_length = kwargs.get('vehicle_name_length')
        self.distance_scale = kwargs.get('distance_scale', 1)
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
