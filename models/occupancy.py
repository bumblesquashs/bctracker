
from enum import Enum

# Based on https://gtfs.org/realtime/reference/#enum-occupancystatus
class Occupancy(Enum):
    EMPTY = 'Empty'
    MANY_SEATS_AVAILABLE = 'Many seats available'
    FEW_SEATS_AVAILABLE = 'Few seats available'
    STANDING_ROOM_ONLY = 'Standing room only'
    CRUSHED_STANDING_ROOM_ONLY = 'Crushed standing room only'
    FULL = 'Full'
    NOT_ACCEPTING_PASSENGERS = 'Not accepting passengers'
    NO_DATA_AVAILABLE = 'Unavailable'
    NOT_BOARDABLE = 'Not boardable'
    
    @property
    def status_class(self):
        match self:
            case Occupancy.EMPTY:
                return 'occupancy-empty'
            case Occupancy.MANY_SEATS_AVAILABLE:
                return 'occupancy-many-seats'
            case Occupancy.FEW_SEATS_AVAILABLE:
                return 'occupancy-few-seats'
            case Occupancy.STANDING_ROOM_ONLY:
                return 'occupancy-standing-room'
            case Occupancy.CRUSHED_STANDING_ROOM_ONLY:
                return 'occupancy-crushed'
            case Occupancy.FULL:
                return 'occupancy-full'
            case Occupancy.NOT_ACCEPTING_PASSENGERS:
                return 'occupancy-unavailable'
            case Occupancy.NO_DATA_AVAILABLE:
                return 'occupancy-unavailable'
            case Occupancy.NOT_BOARDABLE:
                return 'occupancy-unavailable'
    
    @property
    def icon(self):
        match self:
            case Occupancy.EMPTY:
                return 'no-people'
            case Occupancy.MANY_SEATS_AVAILABLE:
                return 'one-person'
            case Occupancy.FEW_SEATS_AVAILABLE:
                return 'two-people'
            case Occupancy.STANDING_ROOM_ONLY:
                return 'two-people'
            case Occupancy.CRUSHED_STANDING_ROOM_ONLY:
                return 'three-people'
            case Occupancy.FULL:
                return 'three-people'
            case Occupancy.NOT_ACCEPTING_PASSENGERS:
                return 'no-people'
            case Occupancy.NO_DATA_AVAILABLE:
                return 'one-person'
            case Occupancy.NOT_BOARDABLE:
                return 'no-people'
    
    def __str__(self):
        return self.value
