
class Agency:
    '''A company or entity that runs transit'''
    
    __slots__ = (
        'id',
        'name',
        'gtfs_url',
        'realtime_url',
        'enabled',
        'prefix_headsigns',
        'accurate_seconds'
    )
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS is enabled for this agency'''
        return self.enabled and self.gtfs_url
    
    @property
    def realtime_enabled(self):
        '''Checks if realtime is enabled for this agency'''
        return self.enabled and self.realtime_url
    
    def __init__(self, id, name, gtfs_url=None, realtime_url=None, enabled=True, prefix_headsigns=False, accurate_seconds=True):
        self.id = id
        self.name = name
        self.gtfs_url = gtfs_url
        self.realtime_url = realtime_url
        self.enabled = enabled
        self.prefix_headsigns = prefix_headsigns
        self.accurate_seconds = accurate_seconds
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
