
class Settings:
    
    __slots__ = (
        'cron_id',
        'admin_key',
        'all_systems_domain',
        'system_domain',
        'system_domain_path',
        'cookie_domain',
        'analytics_key',
        'enable_analytics',
        'enable_gtfs_backups',
        'enable_realtime_backups',
        'enable_database_backups',
        'update_cache_in_background'
    )
    
    def __init__(self):
        # Basic settings
        self.cron_id = None
        self.admin_key = None
        
        # Domain settings
        self.all_systems_domain = None
        self.system_domain = None
        self.system_domain_path = None
        self.cookie_domain = None
        
        # Key settings
        self.analytics_key = None
        
        # Functionality settings
        self.enable_analytics = True
        self.enable_gtfs_backups = True
        self.enable_realtime_backups = True
        self.enable_database_backups = True
        self.update_cache_in_background = True
    
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
        self.update_cache_in_background = config.get('update_cache_in_background', 'true') == 'true'
