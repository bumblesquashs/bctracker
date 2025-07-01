
from dataclasses import dataclass

@dataclass(slots=True)
class Settings:
    
    # Basic settings
    cron_id: str = 'bctracker-muncher'
    admin_key: str | None = None
    
    # Domain settings
    all_systems_domain: str | None = None
    system_domain: str | None = None
    system_domain_path: str | None = None
    cookie_domain: str | None = None
    
    # Key settings
    analytics_key: str | None = None
    
    # Functionality settings
    enable_analytics: bool = True
    enable_gtfs_backups: bool = True
    enable_realtime_backups: bool = True
    enable_database_backups: bool = True
    
    def setup(self, config):
        self.cron_id = config.get('cron_id', 'bctracker-muncher')
        self.admin_key = config.get('admin_key')
        
        self.all_systems_domain = config['all_systems_domain']
        self.system_domain = config['system_domain']
        self.system_domain_path = config['system_domain_path']
        self.cookie_domain = config.get('cookie_domain')
        
        self.analytics_key = config.get('analytics_key')
        
        self.enable_analytics = config.get('enable_analytics', 'true') == 'true'
        self.enable_gtfs_backups = config.get('enable_gtfs_backups', 'true') == 'true'
        self.enable_realtime_backups = config.get('enable_realtime_backups', 'true') == 'true'
        self.enable_database_backups = config.get('enable_database_backups', 'true') == 'true'
