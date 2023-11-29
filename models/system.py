
import helpers.overview
import helpers.position
import helpers.region

from models.schedule import Schedule

class System:
    '''A city or region with a defined set of routes, stops, trips, and other relevant data'''
    
    __slots__ = ('id', 'name', 'region', 'enabled', 'visible', 'prefix_headsign', 'recolour_black', 'gtfs_url', 'realtime_url', 'validation_errors', 'last_updated_date', 'last_updated_time', 'timezone', 'blocks', 'routes', 'routes_by_number', 'services', 'sheets', 'stops', 'stops_by_number', 'trips')
    
    @classmethod
    def from_csv(cls, row):
        '''Returns a system initialized from the given CSV row'''
        id = row['system_id']
        name = row['name']
        region = helpers.region.find(row['region_id'])
        enabled = row['enabled'] == '1'
        visible = row['visible'] == '1'
        prefix_headsign = row['prefix_headsign'] == '1'
        recolour_black = row['recolour_black'] == '1'
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
        return cls(id, name, region, enabled, visible, prefix_headsign, recolour_black, gtfs_url, realtime_url)
    
    def __init__(self, id, name, region, enabled, visible, prefix_headsign, recolour_black, gtfs_url, realtime_url):
        self.id = id
        self.name = name
        self.region = region
        self.enabled = enabled
        self.visible = visible
        self.prefix_headsign = prefix_headsign
        self.recolour_black = recolour_black
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
    def is_loaded(self):
        return self.last_updated_date is not None and self.last_updated_time is not None
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS data is enabled for this system'''
        return self.enabled and self.gtfs_url is not None
    
    @property
    def realtime_enabled(self):
        '''Checks if realtime data is enabled for this system'''
        return self.enabled and self.realtime_url is not None
    
    @property
    def schedule(self):
        '''The overall service schedule for this system'''
        return Schedule.combine(self.get_services())
    
    def get_block(self, block_id):
        '''Returns the block with the given ID'''
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None
    
    def get_blocks(self):
        '''Returns all blocks'''
        return sorted(self.blocks.values())
    
    def get_overviews(self):
        '''Returns all overviews'''
        return helpers.overview.find_all(last_seen_system_id=self.id)
    
    def get_positions(self):
        '''Returns all positions'''
        return helpers.position.find_all(system_id=self.id)
    
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
        return self.services.values()
    
    def get_sheets(self, services=None):
        '''Returns all sheets'''
        if services is None:
            return sorted(self.sheets)
        return sorted([s for s in self.sheets if services in s])
    
    def copy_sheets(self, services):
        copies = [s.copy(services) for s in self.get_sheets()]
        return [s for s in copies if s is not None]
    
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
    
    def get_last_updated(self, time_format):
        '''Returns the date/time that realtime data was last updated'''
        date = self.last_updated_date
        time = self.last_updated_time
        if date is None or time is None:
            return 'N/A'
        if date.is_today:
            if time.timezone is None:
                return f'at {time.format_web(time_format)}'
            return f'at {time.format_web(time_format)} {time.timezone_name}'
        return date.format_since()
    
    def search_blocks(self, query):
        '''Returns all blocks that match the given query'''
        return [b.get_match(query) for b in self.blocks.values()]
    
    def search_routes(self, query):
        '''Returns all routes that match the given query'''
        return [r.get_match(query) for r in self.routes.values()]
    
    def search_stops(self, query):
        '''Returns all stops that match the given query'''
        return [s.get_match(query) for s in self.stops.values()]
