
class Agency:
    '''A company or entity that runs transit'''
    
    __slots__ = (
        'id',
        'name',
        'gtfs_url',
        'realtime_url',
        'enabled',
        'prefix_headsigns',
        'accurate_seconds',
        'vehicle_name_length'
    )
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS is enabled for this agency'''
        return self.enabled and self.gtfs_url
    
    @property
    def realtime_enabled(self):
        '''Checks if realtime is enabled for this agency'''
        return self.enabled and self.realtime_url
    
    def __init__(self, id, name, gtfs_url=None, realtime_url=None, enabled=True, prefix_headsigns=False, accurate_seconds=True, vehicle_name_length=None):
        self.id = id
        self.name = name
        self.gtfs_url = gtfs_url
        self.realtime_url = realtime_url
        self.enabled = enabled
        self.prefix_headsigns = prefix_headsigns
        self.accurate_seconds = accurate_seconds
        self.vehicle_name_length = vehicle_name_length
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
    
    def get_gtfs_url(self, system):
        if self.gtfs_enabled:
            url = self.gtfs_url
            if system.remote_id:
                url = url.replace('$REMOTE_ID', str(system.remote_id))
            return url
        return None
    
    def get_realtime_url(self, system):
        if self.realtime_enabled:
            url = self.realtime_url
            if system.remote_id:
                url = url.replace('$REMOTE_ID', str(system.remote_id))
            return url
        return None
