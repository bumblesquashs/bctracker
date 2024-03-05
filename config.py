
# Basic config
cron_id = None
admin_key = None

# Domain config
global_domain = None
system_domain = None
system_domain_path = None
agency_domain = None
agency_domain_path = None
cookie_domain = None

# Key config
analytics_key = None

# Functionality config
enable_analytics = True
enable_gtfs_backups = True
enable_realtime_backups = True
enable_database_backups = True

def setup(config):
    global cron_id, admin_key
    cron_id = config.get('cron_id', 'bctracker-muncher')
    admin_key = config.get('admin_key')
    
    global global_domain, system_domain, system_domain_path, agency_domain, agency_domain_path, cookie_domain
    global_domain = config['global_domain']
    system_domain = config['system_domain']
    system_domain_path = config['system_domain_path']
    agency_domain = config['agency_domain']
    agency_domain_path = config['agency_domain_path']
    cookie_domain = config.get('cookie_domain')
    
    global analytics_key
    analytics_key = config.get('analytics_key')
    
    global enable_analytics, enable_gtfs_backups, enable_realtime_backups, enable_database_backups
    enable_analytics = config.get('enable_analytics', 'true') == 'true'
    enable_gtfs_backups = config.get('enable_gtfs_backups', 'true') == 'true'
    enable_realtime_backups = config.get('enable_realtime_backups', 'true') == 'true'
    enable_database_backups = config.get('enable_database_backups', 'true') == 'true'
