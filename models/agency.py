
class Agency:
    '''A company or entity that runs transit'''
    
    __slots__ = (
        'id',
        'name',
        'enabled',
        'prefix_headsigns',
        'gtfs_url',
        'realtime_url'
    )
    
    @classmethod
    def from_csv(cls, row):
        '''Returns an agency initialized from the given CSV row'''
        id = row['agency_id']
        name = row['name']
        enabled = row['enabled'] == '1'
        prefix_headsigns = row['prefix_headsigns'] == '1'
        gtfs_url = row['gtfs_url']
        if gtfs_url == '':
            gtfs_url = None
        realtime_url = row['realtime_url']
        if realtime_url == '':
            realtime_url = None
        return cls(id, name, enabled, prefix_headsigns, gtfs_url, realtime_url)
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS is enabled for this agency'''
        return self.enabled and self.gtfs_url
    
    @property
    def realtime_enabled(self):
        '''Checks if realtime is enabled for this agency'''
        return self.enabled and self.realtime_url
    
    def __init__(self, id, name, enabled, prefix_headsigns, gtfs_url, realtime_url):
        self.id = id
        self.name = name
        self.enabled = enabled
        self.prefix_headsigns = prefix_headsigns
        self.gtfs_url = gtfs_url
        self.realtime_url = realtime_url
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
