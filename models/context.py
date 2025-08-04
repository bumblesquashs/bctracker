
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.agency import Agency
    from models.bus import Bus
    from models.system import System

from dataclasses import dataclass

from constants import *

import repositories

@dataclass(init=False, slots=True)
class Context:
    '''A context representing an agency and system'''
    
    agency: Agency | None
    system: System | None
    
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
    def gtfs_enabled(self):
        if self.system:
            return self.system.gtfs_enabled
        if self.agency:
            return self.agency.gtfs_enabled
        return True
    
    @property
    def realtime_enabled(self):
        if self.system:
            return self.system.realtime_enabled
        if self.agency:
            return self.agency.realtime_enabled
        return True
    
    @property
    def gtfs_loaded(self):
        if self.system:
            return self.system.gtfs_loaded
        return False
    
    @property
    def realtime_loaded(self):
        if self.system:
            return self.system.realtime_loaded
        return False
    
    @property
    def timezone(self):
        if self.system:
            return self.system.timezone
        return DEFAULT_TIMEZONE
    
    @property
    def prefix_headsigns(self):
        if self.agency:
            return self.agency.prefix_headsigns
        return DEFAULT_PREFIX_HEADSIGNS
    
    @property
    def accurate_seconds(self):
        if self.agency:
            return self.agency.accurate_seconds
        return DEFAULT_ACCURATE_SECONDS
    
    @property
    def prefer_route_id(self):
        if self.agency:
            return self.agency.prefer_route_id
        return DEFAULT_PREFER_ROUTE_ID
    
    @property
    def prefer_stop_id(self):
        if self.agency:
            return self.agency.prefer_stop_id
        return DEFAULT_PREFER_STOP_ID
    
    @property
    def show_stop_number(self):
        if self.agency:
            return self.agency.show_stop_number
        return DEFAULT_SHOW_STOP_NUMBER
    
    @property
    def vehicle_name_length(self):
        if self.agency:
            return self.agency.vehicle_name_length
        return DEFAULT_VEHICLE_NAME_LENGTH
    
    @property
    def distance_scale(self):
        if self.agency:
            return self.agency.distance_scale
        return DEFAULT_DISTANCE_SCALE
    
    @property
    def enable_blocks(self):
        if self.agency:
            return self.agency.enable_blocks
        return DEFAULT_ENABLE_BLOCKS
    
    def __init__(self, agency: Agency | None = None, system: System | None = None):
        if agency and system and agency != system.agency:
            raise ValueError('Agency mismatch')
        if system and not agency:
            agency = system.agency
        self.agency = agency
        self.system = system
    
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
    
    def without_system(self):
        return Context(self.agency)
    
    def find_bus(self, id: str) -> Bus:
        return repositories.order.find_bus(self, id)
    
    def search_placeholder_text(self):
        '''Search placeholder text to display for this context'''
        if self.system:
            values = []
            if self.realtime_enabled:
                values.append('buses')
            values.append('routes')
            values.append('stops')
            if self.enable_blocks:
                values.append('blocks')
            if len(values) == 1:
                return f'Search for {self} {values[0]}'
            if len(values) == 2:
                return f'Search for {self} {values[0]} and {values[1]}'
            values_string = ', '.join(values[:-1])
            return f'Search for {self} {values_string}, and {values[-1]}'
        return 'Search for buses in all systems'
