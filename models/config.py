
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
    enable_route_variants: bool = True
    enable_stacked_headsigns: bool = False
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
    realtime_update_frequency: int = 1
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
        if self.realtime_enabled and self.realtime_url:
            url = self.realtime_url
            if '$REMOTE_ID' in url and self.remote_id:
                url = url.replace('$REMOTE_ID', str(self.remote_id))
            if '$TRANSLINK_API_KEY' in url and settings.current.translink_api_key:
                url = url.replace('$TRANSLINK_API_KEY', str(settings.current.translink_api_key))
            return url
        return None
