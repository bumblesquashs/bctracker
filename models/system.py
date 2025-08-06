
from dataclasses import dataclass, field
import pytz

from models.agency import Agency
from models.backoff import Backoff
from models.block import Block
from models.context import Context
from models.date import Date
from models.region import Region
from models.route import Route, RouteCache
from models.schedule import Schedule
from models.service import Service
from models.sheet import Sheet
from models.stop import Stop, StopCache
from models.trip import Trip, TripCache

import repositories

from constants import DEFAULT_TIMEZONE

@dataclass(slots=True)
class System:
    '''A city or region with a defined set of routes, stops, trips, and other relevant data'''
    
    id: str
    agency: Agency
    region: Region
    name: str
    
    remote_id: int | None = None
    enabled: bool = True
    timezone: pytz.BaseTzInfo = DEFAULT_TIMEZONE
    colour_routes: str | None = None
    enable_force_gtfs: bool = True
    
    gtfs_downloaded: bool | None = field(default=None, init=False)
    gtfs_loaded: bool = field(default=False, init=False)
    reload_backoff: Backoff = field(init=False)
    last_updated: Date | None = field(default=None, init=False)
    
    blocks: dict[str, Block] = field(default_factory=dict, init=False)
    routes: dict[str, Route] = field(default_factory=dict, init=False)
    routes_by_number: dict[str, Route] = field(default_factory=dict, init=False)
    services: dict[str, Service] = field(default_factory=dict, init=False)
    sheets: list[Sheet] = field(default_factory=list, init=False)
    stops: dict[str, Stop] = field(default_factory=dict, init=False)
    stops_by_number: dict[str, Stop] = field(default_factory=dict, init=False)
    trips: dict[str, Trip] = field(default_factory=dict, init=False)
    
    route_caches: dict[str, RouteCache] = field(default_factory=dict, init=False)
    stop_caches: dict[str, StopCache] = field(default_factory=dict, init=False)
    trip_caches: dict[str, TripCache] = field(default_factory=dict, init=False)
    
    @property
    def context(self):
        return Context(system=self)
    
    @property
    def realtime_loaded(self):
        '''Checks if realtime data has been loaded'''
        return self.last_updated is not None
    
    @property
    def gtfs_enabled(self):
        '''Checks if GTFS data is enabled for this system'''
        return self.enabled and self.agency.gtfs_enabled
    
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
        return self.enabled and self.agency.realtime_enabled
    
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
        services = [s for s in self.get_services() if s.schedule.dates]
        return Schedule.combine(services)
    
    def __post_init__(self):
        self.reload_backoff = Backoff(max_target=2**8)
    
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
    
    def get_block(self, block_id):
        '''Returns the block with the given ID'''
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None
    
    def get_blocks(self):
        '''Returns all blocks'''
        return sorted(self.blocks.values())
    
    def get_allocations(self):
        '''Returns all allocations'''
        return repositories.allocation.find_all(self.context, active=True)
    
    def get_positions(self):
        '''Returns all positions'''
        return repositories.position.find_all(self.context)
    
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
    
    def get_route_cache(self, route_id: str):
        '''Returns the cache for the given route'''
        try:
            return self.route_caches[route_id]
        except KeyError:
            trips = [t for t in self.get_trips() if t.route_id == route_id]
            cache = RouteCache.build(self, trips)
            self.route_caches[route_id] = cache
            return cache
    
    def get_stop_cache(self, stop_id: str):
        '''Returns the cache for the given stop'''
        try:
            return self.stop_caches[stop_id]
        except KeyError:
            departures = repositories.departure.find_all(self.context, stop_id=stop_id)
            cache = StopCache.build(self, departures)
            self.stop_caches[stop_id] = cache
            return cache
    
    def get_trip_cache(self, trip_id: str):
        '''Returns the cache for the given trip'''
        try:
            return self.trip_caches[trip_id]
        except KeyError:
            departures = repositories.departure.find_all(self.context, trip_id=trip_id)
            cache = TripCache.build(departures)
            self.trip_caches[trip_id] = cache
            return cache
    
    def reset_caches(self):
        '''Resets the route, stop, and trip caches'''
        self.route_caches = {}
        self.stop_caches = {}
        self.trip_caches = {}
