
from enum import Enum
from zoneinfo import ZoneInfo

class Province(Enum):
    BC = 'British Columbia'
    AB = 'Alberta'
    
    @property
    def code(self):
        return self.name
    
    @property
    def path_id(self) -> str:
        return self.code.lower()
    
    @property
    def site_name(self) -> str:
        match self:
            case Province.BC:
                return 'BCTracker'
            case Province.AB:
                return 'ABTracker'
    
    @property
    def database_name(self) -> str:
        match self:
            case Province.BC:
                return 'bctracker'
            case Province.AB:
                return 'abtracker'
    
    @property
    def logfile_name(self) -> str:
        match self:
            case Province.BC:
                return 'bctracker'
            case Province.AB:
                return 'abtracker'
    
    @property
    def default_theme_id(self) -> str:
        match self:
            case Province.BC:
                return 'bc-transit'
            case Province.AB:
                return 'calgary-transit'
    
    @property
    def default_timezone(self) -> ZoneInfo:
        match self:
            case Province.BC:
                return ZoneInfo('America/Vancouver')
            case Province.AB:
                return ZoneInfo('America/Edmonton')
    
    def __str__(self):
        return self.value
