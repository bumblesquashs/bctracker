
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.agency import Agency
    from models.system import System
    from models.vehicle import Vehicle

from dataclasses import dataclass

from constants import *

from models.config import Config
from models.date import Date
from models.model import ModelCategory
from models.time import Time
from models.timestamp import Timestamp

import repositories
import settings

@dataclass(init=False, slots=True)
class Context:
    '''A context representing an agency and system'''
    
    agency: Agency | None
    system: System | None
    
    config: Config
    
    @classmethod
    def find(cls, agency_id=None, system_id=None):
        if agency_id:
            agency = repositories.agency.find(agency_id)
        else:
            agency = None
        if system_id:
            system = repositories.system.find(system_id)
        else:
            system = None
        return cls(agency, system)
    
    @property
    def agency_id(self):
        if self.agency:
            return self.agency.id
        return None
    
    @property
    def system_id(self):
        if self.system:
            return self.system.id
        return None
    
    @property
    def gtfs_loaded(self):
        if self.system:
            return self.system.gtfs_loaded
        systems = [s for s in repositories.system.find_all() if s.agency == self.agency]
        return all(s.gtfs_loaded for s in systems)
    
    @property
    def realtime_loaded(self):
        if self.system:
            return self.system.realtime_loaded
        systems = [s for s in repositories.system.find_all() if s.agency == self.agency]
        return all(s.realtime_loaded for s in systems)
    
    @property
    def today(self) -> Date:
        return Date.today(self.config.timezone)
    
    @property
    def now(self) -> Time:
        return Time.now(self.config.timezone, self.config.accurate_seconds)
    
    @property
    def timestamp(self) -> Timestamp:
        return Timestamp.now(self.config.timezone, self.config.accurate_seconds)
    
    def __init__(self, agency: Agency | None = None, system: System | None = None):
        if agency and system and agency != system.agency:
            raise ValueError('Agency mismatch')
        if system and not agency:
            agency = system.agency
        self.agency = agency
        self.system = system
        if system:
            self.config = system.config
        elif agency:
            self.config = agency.config
        else:
            self.config = Config(
                force_gtfs_enabled=True,
                force_realtime_enabled=True,
            )
    
    def __str__(self):
        if self.system:
            return str(self.system)
        if self.agency:
            return str(self.agency)
        return 'All Transit Systems'
    
    def __hash__(self):
        return hash((self.agency, self.system))
    
    def __eq__(self, other):
        return self.agency == other.agency and self.system == other.system
    
    def __lt__(self, other):
        if self.agency == other.agency:
            if not self.system:
                return True
            if not other.system:
                return False
            return self.system < other.system
        if not self.agency:
            return True
        if not other.agency:
            return False
        return self.agency < other.agency
    
    def url(self, *args, **kwargs):
        '''Returns a URL formatted based on the given path'''
        components = []
        tag_component = None
        for arg in args:
            if isinstance(arg, str) and arg.startswith('#'):
                tag_component = arg
                continue
            try:
                components.append(str(arg.url_id))
            except AttributeError:
                components.append(str(arg))
        path = '/'.join(components).rstrip('/')
        query_args = {k:v for k, v in kwargs.items() if v is not None}
        
        if settings.current.root_domain:
            url = settings.current.root_domain.format(path)
        else:
            url = '/' + path
        
        if self.system_id:
            if settings.current.system_domain:
                url = settings.current.system_domain.format(self.system_id, path)
            else:
                query_args['system'] = self.system_id
        elif self.agency_id:
            if self.agency and self.agency.default_system:
                if settings.current.system_domain:
                    url = settings.current.system_domain.format(self.agency.default_system, path)
                else:
                    query_args['system'] = self.agency.default_system
            else:
                if settings.current.agency_domain:
                    url = settings.current.agency_domain.format(self.agency_id, path)
                else:
                    query_args['agency'] = self.agency_id
        
        if query_args:
            query = '&'.join([f'{k}={v}' for k, v in query_args.items()])
            url += f'?{query}'
        if tag_component:
            url += tag_component
        return url
    
    def without_system(self):
        return Context(self.agency)
    
    def find_vehicle(self, id: str) -> Vehicle:
        return repositories.order.find_vehicle(self, id)
    
    def format_model_category(self, count: int = 1):
        match self.config.default_model_category:
            case ModelCategory.BUS:
                return 'Bus' if count == 1 else 'Buses'
            case ModelCategory.TRAIN:
                return 'Train' if count == 1 else 'Trains'
            case ModelCategory.FERRY:
                return 'Vessel' if count == 1 else 'Vessels'
            case ModelCategory.VEHICLE:
                return 'Vehicle' if count == 1 else 'Vehicles'
    
    def search_placeholder_text(self):
        '''Search placeholder text to display for this context'''
        values = []
        if self.config.realtime_enabled:
            values.append(self.format_model_category(2).lower())
        values.append('routes')
        values.append('stops')
        if self.config.enable_blocks:
            values.append('blocks')
        if self.system:
            if len(values) == 1:
                return f'Search for {self} {values[0]}'
            if len(values) == 2:
                return f'Search for {self} {values[0]} and {values[1]}'
            values_string = ', '.join(values[:-1])
            return f'Search for {self} {values_string}, and {values[-1]}'
        if len(values) == 1:
            return f'Search for {values[0]} in all systems'
        if len(values) == 2:
            return f'Search for {values[0]} and {values[1]} in all systems'
        values_string = ', '.join(values[:-1])
        return f'Search for {values_string}, and {values[-1]} in all systems'
