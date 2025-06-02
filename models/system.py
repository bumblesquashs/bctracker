
from dataclasses import dataclass, field
import pytz

from models.agency import Agency
from models.backoff import Backoff
from models.block import Block
from models.context import Context
from models.date import Date
from models.region import Region
from models.schedule import Schedule

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
    
    gtfs_downloaded: bool | None = field(default=None, init=False)
    gtfs_loaded: bool = field(default=False, init=False)
    reload_backoff: bool = field(init=False)
    last_updated: Date | None = field(default=None, init=False)
    
    services: dict = field(default_factory=dict, init=False)
    sheets: list = field(default_factory=list, init=False)
    
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
        return Schedule.combine(self.get_services())
    
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
    
    def get_overviews(self):
        '''Returns all overviews'''
        return repositories.overview.find_all(last_seen_context=self.context)
    
    def get_positions(self):
        '''Returns all positions'''
        return repositories.position.find_all(self.context)
    
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
    
    def search_blocks(self, query):
        '''Returns all blocks that match the given query'''
        context = self.context
        blocks = []
        block_trips = {}
        for trip in repositories.trip.find_all(context):
            block_trips.setdefault(trip.block_id, []).append(trip)
        for block_id, trips in block_trips.items():
            blocks.append(Block(context, block_id, trips))
        return [b.get_match(query) for b in blocks]
    
    def search_routes(self, query):
        '''Returns all routes that match the given query'''
        routes = repositories.route.find_all(self.context)
        return [r.get_match(query) for r in routes]
    
    def search_stops(self, query):
        '''Returns all stops that match the given query'''
        stops = repositories.stop.find_all(self.context)
        return [s.get_match(query) for s in stops]
