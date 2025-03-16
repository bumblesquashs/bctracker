
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.agency import Agency
    from models.system import System

class Context:
    '''A context representing an agency and system'''
    
    __slots__ = (
        'agency',
        'system'
    )
    
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
    def show_stop_number(self):
        if self.agency:
            return self.agency.show_stop_number
        return False
    
    def __init__(self, agency: Agency = None, system: System = None):
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
    
    def __eq__(self, other):
        return self.agency == other.agency and self.system == other.system
