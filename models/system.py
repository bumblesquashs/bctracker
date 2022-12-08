
import helpers.region

from models.schedule import Schedule

class System:
    '''A city or region with a defined set of routes, stops, trips, and other relevant data'''
    
    __slots__ = ('id', 'name', 'region', 'enabled', 'visible', 'prefix_headsign', 'gtfs_url', 'realtime_url', 'validation_errors', 'last_updated_date', 'last_updated_time', 'timezone', 'blocks', 'routes', 'routes_by_number', 'services', 'shapes', 'sheets', 'stops', 'stops_by_number', 'trips')
    
    @classmethod
    def from_csv(cls, row):
        '''Returns a system initialized from the given CSV row'''
        id = row['system_id']
        name = row['name']
        region = helpers.region.find(row['region_id'])
        enabled = row['enabled'] == '1'
        visible = row['visible'] == '1'
        prefix_headsign = row['prefix_headsign'] == '1'
        version = row['version']
        if version == '1':
            remote_id = row['remote_id']
            gtfs_url = f'http://{remote_id}.mapstrat.com/current/google_transit.zip'
            realtime_url = f'http://{remote_id}.mapstrat.com/current/gtfrealtime_VehiclePositions.bin'
        elif version == '2':
            remote_id = row['remote_id']
            gtfs_url = f'https://bct.tmix.se/Tmix.Cap.TdExport.WebApi/gtfs/?operatorIds={remote_id}'
            realtime_url = f'https://bct.tmix.se/gtfs-realtime/vehicleupdates.pb?operatorIds={remote_id}'
        else:
            if 'gtfs_url' in row and row['gtfs_url'] != '':
                gtfs_url = row['gtfs_url']
            else:
                gtfs_url = None
            if 'realtime_url' in row and row['realtime_url'] != '':
                realtime_url = row['realtime_url']
            else:
                realtime_url = None
        return cls(id, name, region, enabled, visible, prefix_headsign, gtfs_url, realtime_url)
    
    def __init__(self, id, name, region, enabled, visible, prefix_headsign, gtfs_url, realtime_url):
        self.id = id
        self.name = name
        self.region = region
        self.enabled = enabled
        self.visible = visible
        self.prefix_headsign = prefix_headsign
        self.gtfs_url = gtfs_url
        self.realtime_url = realtime_url
        
        self.validation_errors = 0
        self.last_updated_date = None
        self.last_updated_time = None
        
        self.timezone = None
        
        self.blocks = {}
        self.routes = {}
        self.routes_by_number = {}
        self.services = {}
        self.shapes = {}
        self.sheets = []
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
    
    @property
    def gtfs_enabled(self):
        '''Whether GTFS data is enabled for this system'''
        return self.enabled and self.gtfs_url is not None
    
    @property
    def realtime_enabled(self):
        '''Whether realtime data is enabled for this system'''
        return self.enabled and self.realtime_url is not None
    
    @property
    def last_updated(self):
        '''Returns the date/time that realtime data was last updated'''
        date = self.last_updated_date
        time = self.last_updated_time
        if date is None or time is None:
            return 'N/A'
        if date.is_today:
            if time.timezone is None:
                return f'at {time}'
            return f'at {time} {time.timezone_name}'
        return date.format_since()
    
    @property
    def schedule(self):
        '''The overall service schedule for this system'''
        return Schedule.combine([s.schedule for s in self.get_services()])
    
    def get_block(self, block_id):
        '''Returns the block with the given ID'''
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None
    
    def get_blocks(self):
        '''Returns all blocks'''
        return sorted(self.blocks.values())
    
    def get_route(self, route_id=None, number=None):
        '''Returns the route with the given ID or number'''
        if route_id is not None and route_id in self.routes:
            return self.routes[route_id]
        if number is not None and number in self.routes_by_number:
            return self.routes_by_number[number]
        return None
    
    def get_routes(self):
        '''Returns all routes'''
        return sorted(self.routes.values())
    
    def get_service(self, service_id):
        '''Returns the service with the given ID'''
        if service_id in self.services:
            return self.services[service_id]
        return None
    
    def get_services(self):
        '''Returns all services'''
        return sorted(self.services.values())
    
    def get_shape(self, shape_id):
        '''Returns the shape with the given ID'''
        if shape_id in self.shapes:
            return self.shapes[shape_id]
        return None
    
    def get_sheets(self):
        '''Returns all sheets'''
        return sorted(self.sheets)
    
    def get_stop(self, stop_id=None, number=None):
        '''Returns the stop with the given ID or number'''
        if stop_id is not None and stop_id in self.stops:
            return self.stops[stop_id]
        if number is not None and number in self.stops_by_number:
            return self.stops_by_number[number]
        return None
    
    def get_stops(self):
        '''Returns all stops'''
        return sorted(self.stops.values())
    
    def get_trip(self, trip_id):
        '''Returns the trip with the given ID'''
        if trip_id in self.trips:
            return self.trips[trip_id]
        return None
    
    def get_trips(self):
        '''Returns all trips'''
        return self.trips.values()
    
    def search_routes(self, query):
        '''Returns all routes that match the given query'''
        matches = [r.get_match(query) for r in self.get_routes()]
        return [m for m in matches if m.value > 0]
    
    def search_stops(self, query):
        '''Returns all stops that match the given query'''
        matches = [s.get_match(query) for s in self.get_stops()]
        return [m for m in matches if m.value > 0]
