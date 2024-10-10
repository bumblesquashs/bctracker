
import pytz

from di import di

from models.backoff import Backoff
from models.route import RouteCache
from models.schedule import Schedule
from models.stop import StopCache
from models.trip import TripCache

from repositories import DepartureRepository, OverviewRepository, PositionRepository

class System:
    '''A city or region with a defined set of routes, stops, trips, and other relevant data'''
    
    __slots__ = (
        'departure_repository',
        'overview_repository',
        'position_repository',
        'id',
        'agency',
        'region',
        'name',
        'remote_id',
        'timezone',
        'colour_routes',
        'gtfs_downloaded',
        'gtfs_loaded',
        'reload_backoff',
        'last_updated',
        'blocks',
        'routes',
        'routes_by_number',
        'services',
        'sheets',
        'stops',
        'stops_by_number',
        'trips',
        'route_caches',
        'stop_caches',
        'trip_caches'
    )
    
    @property
    def realtime_loaded(self):
        '''Checks if realtime data has been loaded'''
        return self.last_updated is not None
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS data is enabled for this system'''
        return self.agency.gtfs_enabled
    
    @property
    def gtfs_url(self):
        '''Returns the URL to load GTFS for this system'''
        if self.gtfs_enabled:
            url = self.agency.gtfs_url
            if self.remote_id:
                url = url.replace('$REMOTE_ID', str(self.remote_id))
            return url
        return None
    
    @property
    def realtime_enabled(self):
        '''Checks if realtime data is enabled for this system'''
        return self.agency.realtime_enabled
    
    @property
    def realtime_url(self):
        '''Returns the URL to load realtime for this system'''
        if self.realtime_enabled:
            url = self.agency.realtime_url
            if self.remote_id:
                url = url.replace('$REMOTE_ID', str(self.remote_id))
            return url
        return None
    
    @property
    def schedule(self):
        '''The overall service schedule for this system'''
        return Schedule.combine(self.get_services())
    
    def __init__(self, id, agency, region, name, **kwargs):
        self.id = id
        self.agency = agency
        self.region = region
        self.name = name
        self.remote_id = kwargs.get('remote_id')
        self.timezone = pytz.timezone(kwargs.get('timezone', 'America/Vancouver'))
        self.colour_routes = kwargs.get('colour_routes')
        
        self.gtfs_downloaded = None
        self.gtfs_loaded = False
        self.reload_backoff = Backoff(max_target=2**8)
        self.last_updated = None
        
        self.blocks = {}
        self.routes = {}
        self.routes_by_number = {}
        self.services = {}
        self.sheets = []
        self.stops = {}
        self.stops_by_number = {}
        self.trips = {}
        
        self.route_caches = {}
        self.stop_caches = {}
        self.trip_caches = {}
        
        self.departure_repository = kwargs.get('departure_repository') or di[DepartureRepository]
        self.overview_repository = kwargs.get('overview_repository') or di[OverviewRepository]
        self.position_repository = kwargs.get('position_repository') or di[PositionRepository]
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
    
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
        return self.overview_repository.find_all(last_seen_system=self)
    
    def get_positions(self):
        '''Returns all positions'''
        return self.position_repository.find_all(self)
    
    def get_route(self, route_id=None, number=None):
        '''Returns the route with the given ID or number'''
        if route_id and route_id in self.routes:
            return self.routes[route_id]
        if number and number in self.routes_by_number:
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
        if services:
            return sorted([s for s in self.sheets if services in s])
        return sorted(self.sheets)
    
    def copy_sheets(self, services):
        copies = [s.copy(services) for s in self.get_sheets()]
        return [s for s in copies if s]
    
    def get_stop(self, stop_id=None, number=None):
        '''Returns the stop with the given ID or number'''
        if stop_id and stop_id in self.stops:
            return self.stops[stop_id]
        if number and number in self.stops_by_number:
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
    
    def search_blocks(self, query):
        '''Returns all blocks that match the given query'''
        return [b.get_match(query) for b in self.blocks.values()]
    
    def search_routes(self, query):
        '''Returns all routes that match the given query'''
        return [r.get_match(query) for r in self.routes.values()]
    
    def search_stops(self, query):
        '''Returns all stops that match the given query'''
        return [s.get_match(query) for s in self.stops.values()]
    
    def update_cache(self):
        '''Loads and caches data from the database'''
        if not self.gtfs_enabled:
            return
        print(f'Updating cached data for {self}')
        try:
            self.route_caches = {}
            self.stop_caches = {}
            self.trip_caches = {}
            departures = self.departure_repository.find_all(self)
            trip_departures = {}
            stop_departures = {}
            for departure in departures:
                trip_departures.setdefault(departure.trip_id, []).append(departure)
                stop_departures.setdefault(departure.stop_id, []).append(departure)
            for trip_id, departures in trip_departures.items():
                if trip_id not in self.trip_caches:
                    self.trip_caches[trip_id] = TripCache(departures)
            for stop_id, departures in stop_departures.items():
                if stop_id not in self.stop_caches:
                    self.stop_caches[stop_id] = StopCache(self, departures)
            route_trips = {}
            for trip in self.get_trips():
                route_trips.setdefault(trip.route_id, []).append(trip)
            for route_id, trips in route_trips.items():
                if route_id not in self.route_caches:
                    self.route_caches[route_id] = RouteCache(self, trips)
        except Exception as e:
            print(f'Failed to update cached data for {self}: {e}')
    
    def get_route_cache(self, route):
        '''Returns the cache for the given route'''
        route_id = getattr(route, 'id', route)
        try:
            return self.route_caches[route_id]
        except KeyError:
            trips = [t for t in self.get_trips() if t.route_id == route_id]
            cache = RouteCache(self, trips)
            self.route_caches[route_id] = cache
            return cache
    
    def get_stop_cache(self, stop):
        '''Returns the cache for the given stop'''
        stop_id = getattr(stop, 'id', stop)
        try:
            return self.stop_caches[stop_id]
        except KeyError:
            departures = self.departure_repository.find_all(self, stop=stop)
            cache = StopCache(self, departures)
            self.stop_caches[stop_id] = cache
            return cache
    
    def get_trip_cache(self, trip):
        '''Returns the cache for the given trip'''
        trip_id = getattr(trip, 'id', trip)
        try:
            return self.trip_caches[trip_id]
        except KeyError:
            departures = self.departure_repository.find_all(self, trip=trip)
            cache = TripCache(departures)
            self.trip_caches[trip_id] = cache
            return cache
