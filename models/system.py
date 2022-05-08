
class System:
    '''A city or region with a defined set of routes, stops, trips, and other relevant data'''
    
    __slots__ = ('id', 'name', 'prefix_headsign', 'gtfs_enabled', 'realtime_enabled', 'gtfs_url', 'realtime_url', 'validation_errors', 'blocks', 'routes', 'routes_by_number', 'services', 'shapes', 'sheets', 'stops', 'stops_by_number', 'trips')
    
    @classmethod
    def from_csv(cls, row):
        id = row['system_id']
        name = row['name']
        prefix_headsign = row['prefix_headsign'] == '1'
        gtfs_enabled = row['gtfs_enabled'] == '1'
        realtime_enabled = row['realtime_enabled'] == '1'
        gtfs_url = row['gtfs_url']
        realtime_url = row['realtime_url']
        return cls(id, name, prefix_headsign, gtfs_enabled, realtime_enabled, gtfs_url, realtime_url)
    
    def __init__(self, id, name, prefix_headsign, gtfs_enabled, realtime_enabled, gtfs_url, realtime_url):
        self.id = id
        self.name = name
        self.prefix_headsign = prefix_headsign
        self.gtfs_enabled = gtfs_enabled
        self.realtime_enabled = realtime_enabled
        self.gtfs_url = gtfs_url
        self.realtime_url = realtime_url
        
        self.validation_errors = 0
        
        self.blocks = {}
        self.routes = {}
        self.routes_by_number = {}
        self.services = {}
        self.shapes = {}
        self.sheets = {}
        self.stops = {}
        self.stops_by_number = {}
        self.trips = {}
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
    
    def get_block(self, block_id):
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None
    
    def get_blocks(self):
        return sorted(self.blocks.values())
    
    def get_route(self, route_id=None, number=None):
        if route_id is not None and route_id in self.routes:
            return self.routes[route_id]
        if number is not None and number in self.routes_by_number:
            return self.routes_by_number[number]
        return None
    
    def get_routes(self):
        return sorted([r for r in self.routes.values() if r.is_current])
    
    def get_service(self, service_id):
        if service_id in self.services:
            return self.services[service_id]
        return None
    
    def get_services(self):
        return sorted(self.services.values())
    
    def get_shape(self, shape_id):
        if shape_id in self.shapes:
            return self.shapes[shape_id]
        return None
    
    def get_sheet(self, service):
        if service.id in self.sheets:
            return self.sheets[service.id]
        return None
    
    def get_sheets(self):
        return sorted({s for s in self.sheets.values() if s.is_current})
    
    def get_stop(self, stop_id=None, number=None):
        if stop_id is not None and stop_id in self.stops:
            return self.stops[stop_id]
        if number is not None and number in self.stops_by_number:
            return self.stops_by_number[number]
        return None
    
    def get_stops(self):
        return [s for s in self.stops.values() if s.is_current]
    
    def get_trip(self, trip_id):
        if trip_id in self.trips:
            return self.trips[trip_id]
        return None
    
    def get_trips(self):
        return self.trips.values()
    
    def search_routes(self, query):
        routes = self.get_routes()
        matches = [r.get_match(query) for r in routes]
        return [m for m in matches if m.value > 0]
    
    def search_stops(self, query):
        stops = self.get_stops()
        matches = [s.get_match(query) for s in stops]
        return [m for m in matches if m.value > 0]
