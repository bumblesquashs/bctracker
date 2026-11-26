
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

from models.model import ModelCategory

import settings

@dataclass
class Config:
    '''Settings available to an agency or system'''
    
    accurate_seconds: bool = True
    ais_colour: str | None = None
    custom_route_colours: dict[str, str] = field(default_factory=dict)
    custom_route_numbers: dict[str, str] = field(default_factory=dict)
    default_model_category: ModelCategory = ModelCategory.VEHICLE
    default_route_colour: str | None = None
    distance_scale: int = 1
    enable_force_gtfs: bool = True
    enable_blocks: bool = True
    enable_realtime_trips: bool = True
    enabled: bool = True
    force_gtfs_enabled: bool = False
    force_realtime_enabled: bool = False
    gtfs_cutoff: str | None = None
    gtfs_url: str | None = None
    ignore_route_colour: str | None = None
    invalid_realtime_percentage: int = 0
    max_invalid_positions: int = 0 
    prefer_route_id: bool = False
    prefer_stop_id: bool = False
    prefix_headsigns: bool = False
    realtime_ais: bool = False
    realtime_url: str | None = None
    remote_id: int | None = None
    show_occupancy: bool = True
    show_stop_number: bool = True
    vehicle_name_length: int | None = None
    timezone: ZoneInfo = field(default_factory=lambda: settings.current.province.default_timezone)

    @property
    def gtfs_enabled(self) -> bool:
        return self.enabled and bool(self.gtfs_url or self.force_gtfs_enabled)

    @property
    def realtime_enabled(self) -> bool:
        return self.enabled and bool(self.realtime_ais or self.realtime_url or self.force_realtime_enabled)
    
    def format_gtfs_url(self):
        if self.gtfs_enabled:
            url = self.gtfs_url
            if self.remote_id:
                url = url.replace('$REMOTE_ID', str(self.remote_id))
            return url
        return None
    
    def format_realtime_url(self):
        '''Returns the URL to load realtime for this system'''
        if self.realtime_enabled:
            url = self.realtime_url
            if self.remote_id:
                url = url.replace('$REMOTE_ID', str(self.remote_id))
            return url
        return None
