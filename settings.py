
from dataclasses import dataclass
from dotenv import load_dotenv

import os

from models.province import Province

from constants import DEFAULT_ADMIN_LOGS_COUNT

@dataclass(slots=True)
class Settings:
    
    # Basic settings
    province: Province = Province.BC
    ais_path: str | None = None
    cron_id: str = 'bctracker-muncher'
    admin_key: str | None = None
    admin_logs_count: int = DEFAULT_ADMIN_LOGS_COUNT
    
    # Domain settings
    root_domain: str | None = None
    system_domain: str | None = None
    agency_domain: str | None = None
    cookie_domain: str | None = None
    
    # Key settings
    analytics_key: str | None = None
    translink_api_key: str | None = None
    
    # Functionality settings
    enable_validation: bool = False
    enable_analytics: bool = True
    enable_gtfs_backups: bool = True
    enable_realtime_backups: bool = True
    enable_database_backups: bool = True
    await_realtime: bool = False
    
    @classmethod
    def from_dotenv(cls):
        load_dotenv()
        
        try:
            province_code = os.getenv('PROVINCE_CODE')
            province = Province[province_code]
        except:
            province = Province.BC
        
        return cls(
            province=province,
            ais_path=os.getenv('AIS_PATH'),
            cron_id=os.getenv('CRON_ID', 'bctracker-muncher'),
            admin_key=os.getenv('ADMIN_KEY'),
            admin_logs_count=int(os.getenv('ADMIN_LOGS_COUNT', DEFAULT_ADMIN_LOGS_COUNT)),
            root_domain=os.getenv('ROOT_DOMAIN'),
            system_domain=os.getenv('SYSTEM_DOMAIN'),
            agency_domain=os.getenv('AGENCY_DOMAIN'),
            cookie_domain=os.getenv('COOKIE_DOMAIN'),
            analytics_key=os.getenv('ANALYTICS_KEY'),
            translink_api_key=os.getenv('TRANSLINK_API_KEY'),
            enable_validation=os.getenv('ENABLE_VALIDATION', 'false') == 'true',
            enable_analytics=os.getenv('ENABLE_ANALYTICS', 'true') == 'true',
            enable_gtfs_backups=os.getenv('ENABLE_GTFS_BACKUPS', 'true') == 'true',
            enable_realtime_backups=os.getenv('ENABLE_REALTIME_BACKUPS', 'true') == 'true',
            enable_database_backups=os.getenv('ENABLE_DATABASE_BACKUPS', 'true') == 'true',
            await_realtime=os.getenv('AWAIT_REALTIME', 'false') == 'true',
        )

current = Settings.from_dotenv()
