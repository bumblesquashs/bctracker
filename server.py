
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, HTTPError, static_file, template, request, response, debug, redirect
from datetime import timedelta
import cherrypy as cp

from di import di
from database import Database
from settings import Settings

from models.bus import Bus
from models.date import Date
from models.event import Event
from models.favourite import Favourite, FavouriteSet

from repositories import *
from services import *

# Increase the version to force CSS reload
VERSION = 39

class Server(Bottle):
    
    __slots__ = (
        'database',
        'settings',
        'adornment_repository',
        'agency_repository',
        'assignment_repository',
        'order_repository',
        'overview_repository',
        'point_repository',
        'position_repository',
        'record_repository',
        'region_repository',
        'route_repository',
        'system_repository',
        'theme_repository',
        'transfer_repository',
        'cron_service',
        'gtfs_service',
        'realtime_service',
        'running'
    )
    
    def __init__(self, database: Database, settings: Settings, **kwargs):
        super().__init__()
        self.running = False
        
        self.database = database
        self.settings = settings
        
        self.adornment_repository = kwargs.get('adornment_repository') or di[AdornmentRepository]
        self.assignment_repository = kwargs.get('assignment_repository') or di[AssignmentRepository]
        self.agency_repository = kwargs.get('agency_repository') or di[AgencyRepository]
        self.order_repository = kwargs.get('order_repository') or di[OrderRepository]
        self.overview_repository = kwargs.get('overview_repository') or di[OverviewRepository]
        self.point_repository = kwargs.get('point_repository') or di[PointRepository]
        self.position_repository = kwargs.get('position_repository') or di[PositionRepository]
        self.record_repository = kwargs.get('record_repository') or di[RecordRepository]
        self.region_repository = kwargs.get('region_repository') or di[RegionRepository]
        self.route_repository = kwargs.get('route_repository') or di[RouteRepository]
        self.system_repository = kwargs.get('system_repository') or di[SystemRepository]
        self.theme_repository = kwargs.get('theme_repository') or di[ThemeRepository]
        self.transfer_repository = kwargs.get('transfer_repository') or di[TransferRepository]
        
        self.cron_service = kwargs.get('cron_service') or di[CronService]
        self.gtfs_service = kwargs.get('gtfs_service') or di[GTFSService]
        self.realtime_service = kwargs.get('realtime_service') or di[RealtimeService]
        
        # Static files
        self.add('/style/<name:path>', append_slash=False, callback=self.style)
        self.add('/img/<name:path>', append_slash=False, callback=self.img)
        self.add('/js/<name:path>', append_slash=False, callback=self.js)
        self.add('/robots.txt', append_slash=False, callback=self.robots_text)
        
        # Pages
        self.add('/', callback=self.home)
        self.add('/news', callback=self.news)
        self.add('/map', callback=self.map)
        self.add('/realtime', callback=self.realtime_all)
        self.add('/realtime/routes', callback=self.realtime_routes)
        self.add('/realtime/models', callback=self.realtime_models)
        self.add('/realtime/speed', callback=self.realtime_speed)
        self.add('/fleet', callback=self.fleet)
        self.add('/bus/<bus_number:int>', callback=self.bus_overview)
        self.add('/bus/<bus_number:int>/map', callback=self.bus_map)
        self.add('/bus/<bus_number:int>/history', callback=self.bus_history)
        self.add('/history', callback=self.history_last_seen)
        self.add('/history/first-seen', callback=self.history_first_seen)
        self.add('/history/transfers', callback=self.history_transfers)
        self.add('/routes', callback=self.routes_list)
        self.add('/routes/map', callback=self.routes_map)
        self.add('/routes/<route_number>', callback=self.route_overview)
        self.add('/routes/<route_number>/map', callback=self.route_map)
        self.add('/routes/<route_number>/schedule', callback=self.route_schedule)
        self.add('/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>', callback=self.route_schedule_date)
        self.add('/blocks', callback=self.blocks)
        self.add('/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>', callback=self.blocks_schedule_date)
        self.add('/blocks/<block_id>', callback=self.block_overview)
        self.add('/blocks/<block_id>/map', callback=self.block_map)
        self.add('/blocks/<block_id>/history', callback=self.block_history)
        self.add('/trips/<trip_id>', callback=self.trip_overview)
        self.add('/trips/<trip_id>/map', callback=self.trip_map)
        self.add('/trips/<trip_id>/history', callback=self.trip_history)
        self.add('/stops', callback=self.stops)
        self.add('/stops/<stop_number>', callback=self.stop_overview)
        self.add('/stops/<stop_number>/map', callback=self.stop_map)
        self.add('/stops/<stop_number>/schedule', callback=self.stop_schedule)
        self.add('/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>', callback=self.stop_schedule_date)
        self.add('/about', callback=self.about)
        self.add('/guide', callback=self.guide)
        self.add('/nearby', callback=self.nearby)
        self.add('/themes', callback=self.themes)
        self.add('/personalize', callback=self.personalize)
        self.add('/systems', callback=self.systems)
        self.add('/admin', require_admin=True, callback=self.admin)
        
        # Frames
        self.add('/frame/nearby', append_slash=False, callback=self.frame_nearby)
        
        # API endpoints
        self.add('/api/health-check', append_slash=False, callback=self.api_health_check)
        self.add('/api/map.json', append_slash=False, callback=self.api_map)
        self.add('/api/shape/<shape_id>.json', append_slash=False, callback=self.api_shape)
        self.add('/api/routes', append_slash=False, callback=self.api_routes)
        self.add('/api/search', method='POST', callback=self.api_search)
        self.add('/api/nearby.json', append_slash=False, callback=self.api_nearby)
        self.add('/api/admin/reload-adornments', method='POST', require_admin=True, callback=self.api_admin_reload_adornments)
        self.add('/api/admin/reload-orders', method='POST', require_admin=True, callback=self.api_admin_reload_orders)
        self.add('/api/admin/reload-systems', method='POST', require_admin=True, callback=self.api_admin_reload_systems)
        self.add('/api/admin/reload-themes', method='POST', require_admin=True, callback=self.api_admin_reload_themes)
        self.add('/api/admin/restart-cron', method='POST', require_admin=True, callback=self.api_admin_restart_cron)
        self.add('/api/admin/backup-database', method='POST', require_admin=True, callback=self.api_admin_backup_database)
        self.add('/api/admin/reload-gtfs/<reload_system_id>', method='POST', require_admin=True, callback=self.api_admin_reload_gtfs)
        self.add('/api/admin/reload-realtime/<reload_system_id>', method='POST', require_admin=True, callback=self.api_admin_reload_realtime)
        
        # Errors
        self.error(403)(self.error_403)
        self.error(404)(self.error_404)
        self.error(500)(self.error_500)
    
    def start(self, args):
        '''Loads all required data and launches the server'''
        self.running = True
        
        cp.config.update('server.conf')
        self.settings.setup(cp.config)
        
        self.database.connect()
            
        if args.debug:
            print('Starting bottle in DEBUG mode')
            debug(True)
        if args.reload:
            print('Forcing GTFS redownload')
        if args.updatedb:
            print('Forcing database refresh')
        
        self.adornment_repository.load()
        self.order_repository.load()
        self.system_repository.load()
        self.theme_repository.load()
        
        self.position_repository.delete_all()
        
        handler = TimedRotatingFileHandler(filename='logs/access_log.log', when='d', interval=7)
        log = WSGILogger(self, [handler], ApacheFormatter())
        
        cp.tree.graft(log, '/')
        cp.server.start()
        
        for system in self.system_repository.find_all():
            if self.running:
                self.gtfs_service.load(system, args.reload, args.updatedb)
                if not self.gtfs_service.validate(system):
                    self.gtfs_service.load(system, True)
                self.gtfs_service.update_cache_in_background(system)
                self.realtime_service.update(system)
                if not self.realtime_service.validate(system):
                    system.validation_errors += 1
        if self.running:
            self.realtime_service.update_records()
            self.cron_service.start()
    
    def stop(self):
        '''Terminates the server'''
        self.running = False
        self.cron_service.stop()
        self.database.disconnect()
        if cp.server.running:
            cp.server.stop()
    
    def get_url(self, system, path='', **kwargs):
        '''Returns a URL formatted based on the given system and path'''
        system_id = getattr(system, 'id', system)
        if system_id:
            url = self.settings.system_domain.format(system_id, path).rstrip('/')
        else:
            url = self.settings.all_systems_domain.format(path).rstrip('/')
        query_args = {k:v for k, v in kwargs.items() if v is not None}
        if query_args:
            query = '&'.join([f'{k}={v}' for k, v in query_args.items()])
            url += f'?{query}'
        return url
    
    def validate_admin(self):
        '''Checks if the admin key in the query/cookie matches the expected admin key'''
        return not self.settings.admin_key or self.query_cookie('admin_key', max_age_days=1) == self.settings.admin_key
    
    def page(self, name, title, path='', path_args=None, system=None, agency=None, enable_refresh=True, include_maps=False, full_map=False, **kwargs):
        '''Returns an HTML page with the given name and details'''
        is_admin = self.validate_admin()
        
        theme_id = request.query.get('theme') or request.get_cookie('theme')
        time_format = request.query.get('time_format') or request.get_cookie('time_format')
        bus_marker_style = request.query.get('bus_marker_style') or request.get_cookie('bus_marker_style')
        hide_systems = request.get_cookie('hide_systems') == 'yes'
        if system:
            last_updated = system.get_last_updated(time_format)
        else:
            last_updated = self.realtime_service.get_last_updated(time_format)
        return template(f'pages/{name}',
            di=di,
            settings=self.settings,
            version=VERSION,
            title=title,
            path=path,
            path_args=path_args or {},
            system=system,
            agency=agency,
            enable_refresh=enable_refresh,
            include_maps=include_maps,
            full_map=full_map,
            regions=self.region_repository.find_all(),
            systems=self.system_repository.find_all(),
            is_admin=is_admin,
            get_url=self.get_url,
            last_updated=last_updated,
            theme=self.theme_repository.find(theme_id),
            time_format=time_format,
            bus_marker_style=bus_marker_style,
            hide_systems=hide_systems,
            show_speed=request.get_cookie('speed') == '1994',
            **kwargs
        )
    
    def error_page(self, name, title, path='', path_args=None, system=None, agency=None, **kwargs):
        '''Returns an error page with the given name and details'''
        return self.page(
            name=f'errors/{name}',
            title=title,
            path=path,
            path_args=path_args,
            system=system,
            agency=agency,
            enable_refresh=False,
            **kwargs
        )
    
    def frame(self, name, system, agency, **kwargs):
        '''Returns an HTML element that can be inserted into a page'''
        return template(f'frames/{name}',
            system=system,
            agency=agency,
            get_url=self.get_url,
            time_format=request.get_cookie('time_format'),
            show_speed=request.get_cookie('speed') == '1994',
            **kwargs
        )
    
    def set_cookie(self, key, value, max_age_days=3650):
        '''Creates a cookie using the given key and value'''
        max_age = 60 * 60 * 24 * max_age_days
        if self.settings.cookie_domain:
            response.set_cookie(key, value, max_age=max_age, domain=self.settings.cookie_domain, path='/')
        else:
            response.set_cookie(key, value, max_age=max_age, path='/')
    
    def query_cookie(self, key, default_value=None, max_age_days=3650):
        '''Creates a cookie if a query value exists, otherwise uses the existing cookie value'''
        value = request.query.get(key)
        if value is not None:
            self.set_cookie(key, value, max_age_days)
            return value
        return request.get_cookie(key, default_value)
    
    def get_favourites(self):
        '''Returns the current set of favourites stored in the cookie'''
        favourites_string = request.get_cookie('favourites', '')
        return FavouriteSet.parse(favourites_string)
    
    def add(self, base_path, method='GET', append_slash=True, require_admin=False, system_key='system_id', callback=None):
        '''Adds an endpoint to the server'''
        if not callback:
            return
        paths = [base_path]
        if base_path == '/':
            paths.append(f'/<{system_key}>')
            if append_slash:
                paths.append(f'/<{system_key}>/')
        else:
            paths.append(f'/<{system_key}>{base_path}')
            if append_slash:
                paths.append(f'{base_path}/')
                paths.append(f'/<{system_key}>{base_path}/')
        def endpoint(*args, **kwargs):
            if require_admin and not self.validate_admin():
                raise HTTPError(403)
            if system_key in kwargs:
                system_id = kwargs[system_key]
                system = self.system_repository.find(system_id)
                if not system:
                    raise HTTPError(404)
                del kwargs[system_key]
            else:
                system = None
            agency = self.agency_repository.find('bc-transit')
            return callback(system=system, agency=agency, *args, **kwargs)
        self.route(paths, method, callback=endpoint)
    
    # =============================================================
    # Static Files
    # =============================================================
    
    def style(self, system, agency, name):
        return static_file(name, root='./style')
    
    def img(self, system, agency, name):
        return static_file(name, root='./img')
    
    def js(self, system, agency, name):
        return static_file(name, root='./js')
    
    def robots_text(self, system, agency):
        return static_file('robots.txt', root='.')
    
    # =============================================================
    # Pages
    # =============================================================
    
    def home(self, system, agency):
        return self.page(
            name='home',
            title='Home',
            system=system,
            agency=agency,
            enable_refresh=False,
            favourites=self.get_favourites()
        )
    
    def news(self, system, agency):
        return self.page(
            name='news',
            title='News Archive',
            path='news',
            system=system,
            agency=agency,
            enable_refresh=False
        )
    
    def map(self, system, agency):
        positions = self.position_repository.find_all(system, has_location=True)
        auto_refresh = self.query_cookie('auto_refresh', 'false') != 'false'
        show_route_lines = self.query_cookie('show_route_lines', 'false') != 'false'
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        visible_positions = positions if show_nis else [p for p in positions if p.trip]
        return self.page(
            name='map',
            title='Map',
            path='map',
            system=system,
            agency=agency,
            include_maps=len(visible_positions) > 0,
            full_map=len(visible_positions) > 0,
            positions=sorted(positions, key=lambda p: p.lat),
            auto_refresh=auto_refresh,
            show_route_lines=show_route_lines,
            show_nis=show_nis,
            visible_positions=visible_positions
        )
    
    def realtime_all(self, system, agency):
        positions = self.position_repository.find_all(system)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            name='realtime/all',
            title='Realtime',
            path='realtime',
            system=system,
            agency=agency,
            positions=positions,
            show_nis=show_nis
        )
    
    def realtime_routes(self, system, agency):
        positions = self.position_repository.find_all(system)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            name='realtime/routes',
            title='Realtime',
            path='realtime/routes',
            system=system,
            agency=agency,
            positions=positions,
            show_nis=show_nis
        )
    
    def realtime_models(self, system, agency):
        positions = self.position_repository.find_all(system)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            name='realtime/models',
            title='Realtime',
            path='realtime/models',
            system=system,
            agency=agency,
            positions=positions,
            show_nis=show_nis
        )
    
    def realtime_speed(self, system, agency):
        self.set_cookie('speed', '1994')
        positions = self.position_repository.find_all(system)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            name='realtime/speed',
            title='Realtime',
            path='realtime/speed',
            system=system,
            agency=agency,
            positions=positions,
            show_nis=show_nis
        )
    
    def fleet(self, system, agency):
        orders = self.order_repository.find_all(agency)
        overviews = self.overview_repository.find_all()
        return self.page(
            name='fleet',
            title='Fleet',
            path='fleet',
            system=system,
            agency=agency,
            orders=[o for o in sorted(orders) if o.visible],
            overviews={o.bus.number: o for o in overviews}
        )
    
    def bus_overview(self, system, agency, bus_number):
        bus = Bus.find(agency, bus_number)
        overview = self.overview_repository.find(bus)
        if (not bus.order and not overview) or not bus.visible:
            return self.error_page(
                name='invalid_bus',
                title='Unknown Bus',
                system=system,
                agency=agency,
                bus_number=bus_number
            )
        position = self.position_repository.find(bus)
        records = self.record_repository.find_all(bus=bus, limit=20)
        return self.page(
            name='bus/overview',
            title=f'Bus {bus}',
            system=system,
            agency=agency,
            include_maps=bool(position),
            bus=bus,
            position=position,
            records=records,
            overview=overview,
            favourite=Favourite('vehicle', bus),
            favourites=self.get_favourites()
        )
    
    def bus_map(self, system, agency, bus_number):
        bus = Bus.find(agency, bus_number)
        overview = self.overview_repository.find(bus)
        if (not bus.order and not overview) or not bus.visible:
            return self.error_page(
                name='invalid_bus',
                title='Unknown Bus',
                system=system,
                agency=agency,
                bus_number=bus_number
            )
        position = self.position_repository.find(bus)
        return self.page(
            name='bus/map',
            title=f'Bus {bus}',
            system=system,
            agency=agency,
            include_maps=bool(position),
            full_map=bool(position),
            bus=bus,
            position=position,
            favourite=Favourite('vehicle', bus),
            favourites=self.get_favourites()
        )
    
    def bus_history(self, system, agency, bus_number):
        bus = Bus.find(agency, bus_number)
        overview = self.overview_repository.find(bus)
        if (not bus.order and not overview) or not bus.visible:
            return self.error_page(
                name='invalid_bus',
                title='Unknown Bus',
                system=system,
                agency=agency,
                bus_number=bus_number
            )
        try:
            page = int(request.query['page'])
        except (KeyError, ValueError):
            page = 1
        items_per_page = 100
        total_items = self.record_repository.count(bus=bus)
        if page < 1:
            records = []
        else:
            records = self.record_repository.find_all(bus=bus, limit=items_per_page, page=page)
        transfers = self.transfer_repository.find_all(bus=bus)
        events = []
        if overview:
            events.append(Event(overview.first_seen_date, 'First Seen'))
            if overview.first_record:
                events.append(Event(overview.first_record.date, 'First Tracked'))
            events.append(Event(overview.last_seen_date, 'Last Seen'))
            if overview.last_record:
                events.append(Event(overview.last_record.date, 'Last Tracked'))
            for transfer in transfers:
                events.append(Event(transfer.date, 'Transferred',  f'{transfer.old_system} to {transfer.new_system}'))
        return self.page(
            name='bus/history',
            title=f'Bus {bus}',
            system=system,
            agency=agency,
            bus=bus,
            records=records,
            overview=overview,
            events=events,
            favourite=Favourite('vehicle', bus),
            favourites=self.get_favourites(),
            page=page,
            items_per_page=items_per_page,
            total_items=total_items
        )
    
    def history_last_seen(self, system, agency):
        overviews = [o for o in self.overview_repository.find_all(system) if o.last_record and o.bus.visible]
        try:
            days = int(request.query['days'])
        except (KeyError, ValueError):
            days = None
        if days:
            try:
                date = Date.today(system.timezone) - timedelta(days=days)
            except AttributeError:
                date = Date.today() - timedelta(days=days)
            overviews = [o for o in overviews if o.last_record.date > date]
        return self.page(
            name='history/last_seen',
            title='Vehicle History',
            path='history',
            path_args={
                'days': days
            },
            system=system,
            agency=agency,
            overviews=sorted(overviews, key=lambda o: o.bus),
            days=days
        )
    
    def history_first_seen(self, system, agency):
        overviews = [o for o in self.overview_repository.find_all(system) if o.first_record and o.bus.visible]
        return self.page(
            name='history/first_seen',
            title='Vehicle History',
            path='history/first-seen',
            system=system,
            agency=agency,
            overviews=sorted(overviews, key=lambda o: (o.first_record.date, o.first_record.first_seen, o.bus), reverse=True)
        )
    
    def history_transfers(self, system, agency):
        filter = request.query.get('filter')
        if filter == 'from':
            transfers = self.transfer_repository.find_all(old_system=system)
        elif filter == 'to':
            transfers = self.transfer_repository.find_all(new_system=system)
        else:
            transfers = self.transfer_repository.find_all(old_system=system, new_system=system)
        return self.page(
            name='history/transfers',
            title='Vehicle History',
            path='history/transfers',
            system=system,
            agency=agency,
            transfers=[t for t in transfers if t.bus.visible],
            filter=filter
        )
    
    def routes_list(self, system, agency):
        return self.page(
            name='routes/list',
            title='Routes',
            path='routes',
            system=system,
            agency=agency,
            enable_refresh=False
        )
    
    def routes_map(self, system, agency):
        routes = self.route_repository.find_all(system)
        show_route_numbers = self.query_cookie('show_route_numbers', 'true') != 'false'
        return self.page(
            name='routes/map',
            title='Routes',
            path='routes/map',
            system=system,
            agency=agency,
            enable_refresh=False,
            include_maps=len(routes) > 0,
            full_map=len(routes) > 0,
            routes=routes,
            show_route_numbers=show_route_numbers
        )
    
    def route_overview(self, system, agency, route_number):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'routes/{route_number}',
                system=system,
                agency=agency
            )
        route = system.get_route(number=route_number)
        if not route:
            return self.error_page(
                name='invalid_route',
                title='Unknown Route',
                system=system,
                agency=agency,
                route_number=route_number
            )
        trips = sorted(route.get_trips(date=Date.today(system.timezone)))
        return self.page(
            name='route/overview',
            title=str(route),
            system=system,
            agency=agency,
            include_maps=len(route.trips) > 0,
            route=route,
            trips=trips,
            recorded_today=self.record_repository.find_recorded_today(system, trips),
            assignments=self.assignment_repository.find_all(system, route=route),
            positions=self.position_repository.find_all(system, route=route),
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_map(self, system, agency, route_number):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'routes/{route_number}/map',
                system=system,
                agency=agency
            )
        route = system.get_route(number=route_number)
        if not route:
            return self.error_page(
                name='invalid_route',
                title='Unknown Route',
                system=system,
                agency=agency,
                route_number=route_number
            )
        return self.page(
            name='route/map',
            title=str(route),
            system=system,
            agency=agency,
            include_maps=len(route.trips) > 0,
            full_map=len(route.trips) > 0,
            route=route,
            positions=self.position_repository.find_all(system, route=route),
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_schedule(self, system, agency, route_number):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'routes/{route_number}/schedule',
                system=system,
                agency=agency
            )
        route = system.get_route(number=route_number)
        if not route:
            return self.error_page(
                name='invalid_route',
                title='Unknown Route',
                system=system,
                agency=agency,
                route_number=route_number
            )
        return self.page(
            name='route/schedule',
            title=str(route),
            system=system,
            agency=agency,
            enable_refresh=False,
            route=route,
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_schedule_date(self, system, agency, route_number, date_string):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'routes/{route_number}/schedule',
                system=system,
                agency=agency
            )
        route = system.get_route(number=route_number)
        if not route:
            return self.error_page(
                name='invalid_route',
                title='Unknown Route',
                system=system,
                agency=agency,
                route_number=route_number
            )
        date = Date.parse(date_string, system.timezone)
        return self.page(
            name='route/date',
            title=str(route),
            system=system,
            agency=agency,
            enable_refresh=False,
            route=route,
            date=date,
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def blocks(self, system, agency):
        return self.page(
            name='blocks/list',
            title='Blocks',
            path='blocks',
            system=system,
            agency=agency,
            enable_refresh=False
        )
    
    def blocks_schedule_date(self, system, agency, date_string):
        try:
            date = Date.parse(date_string, system.timezone)
        except AttributeError:
            date = Date.parse(date_string)
        return self.page(
            name='blocks/date',
            title='Blocks',
            path=f'blocks/schedule/{date_string}',
            system=system,
            agency=agency,
            enable_reload=False,
            date=date
        )
    
    def block_overview(self, system, agency, block_id):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'blocks/{block_id}',
                system=system,
                agency=agency
            )
        block = system.get_block(block_id)
        if not block:
            return self.error_page(
                name='invalid_block',
                title='Unknown Block',
                system=system,
                agency=agency,
                block_id=block_id
            )
        return self.page(
            name='block/overview',
            title=f'Block {block.id}',
            system=system,
            agency=agency,
            include_maps=True,
            block=block,
            positions=self.position_repository.find_all(system, block=block),
            assignment=self.assignment_repository.find(system, block)
        )
    
    def block_map(self, system, agency, block_id):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'blocks/{block_id}/map',
                system=system,
                agency=agency
            )
        block = system.get_block(block_id)
        if not block:
            return self.error_page(
                name='invalid_block',
                title='Unknown Block',
                system=system,
                agency=agency,
                block_id=block_id
            )
        return self.page(
            name='block/map',
            title=f'Block {block.id}',
            system=system,
            agency=agency,
            include_maps=True,
            full_map=True,
            block=block,
            positions=self.position_repository.find_all(system, block=block)
        )
    
    def block_history(self, system, agency, block_id):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'blocks/{block_id}/history',
                system=system,
                agency=agency
            )
        block = system.get_block(block_id)
        if not block:
            return self.error_page(
                name='invalid_block',
                title='Unknown Block',
                system=system,
                agency=agency,
                block_id=block_id
            )
        records = self.record_repository.find_all(system, block=block)
        events = []
        if records:
            events.append(Event(records[0].date, 'Last Tracked'))
            events.append(Event(records[-1].date, 'First Tracked'))
        return self.page(
            name='block/history',
            title=f'Block {block.id}',
            system=system,
            agency=agency,
            block=block,
            records=records,
            events=events
        )
    
    def trip_overview(self, system, agency, trip_id):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'trips/{trip_id}',
                system=system,
                agency=agency
            )
        trip = system.get_trip(trip_id)
        if not trip:
            return self.error_page(
                name='invalid_trip',
                title='Unknown Trip',
                system=system,
                agency=agency,
                trip_id=trip_id
            )
        return self.page(
            name='trip/overview',
            title=f'Trip {trip.id}',
            system=system,
            agency=agency,
            include_maps=True,
            trip=trip,
            positions=self.position_repository.find_all(system, trip=trip),
            assignment=self.assignment_repository.find(system, trip.block_id)
        )
    
    def trip_map(self, system, agency, trip_id):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'trips/{trip_id}/map',
                system=system,
                agency=agency
            )
        trip = system.get_trip(trip_id)
        if not trip:
            return self.error_page(
                name='invalid_trip',
                title='Unknown Trip',
                system=system,
                agency=agency,
                trip_id=trip_id
            )
        return self.page(
            name='trip/map',
            title=f'Trip {trip.id}',
            system=system,
            agency=agency,
            include_maps=True,
            full_map=True,
            trip=trip,
            positions=self.position_repository.find_all(system, trip=trip)
        )
    
    def trip_history(self, system, agency, trip_id):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'trips/{trip_id}/history',
                system=system,
                agency=agency
            )
        trip = system.get_trip(trip_id)
        if not trip:
            return self.error_page(
                name='invalid_trip',
                title='Unknown Trip',
                system=system,
                agency=agency,
                trip_id=trip_id
            )
        records = self.record_repository.find_all(system, trip=trip)
        events = []
        if records:
            events.append(Event(records[0].date, 'Last Tracked'))
            events.append(Event(records[-1].date, 'First Tracked'))
        return self.page(
            name='trip/history',
            title=f'Trip {trip.id}',
            system=system,
            agency=agency,
            trip=trip,
            records=records,
            events=events
        )
    
    def stops(self, system, agency):
        path_args = {}
        search = request.query.get('search')
        if search:
            path_args['search'] = search
        return self.page(
            name='stops',
            title='Stops',
            path='stops',
            path_args=path_args,
            system=system,
            agency=agency,
            enable_refresh=False,
            search=search
        )
    
    def stop_overview(self, system, agency, stop_number):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'stops/{stop_number}',
                system=system,
                agency=agency
            )
        stop = system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                name='invalid_stop',
                title='Unknown Stop',
                system=system,
                agency=agency,
                stop_number=stop_number
            )
        departures = stop.find_departures(date=Date.today(system.timezone))
        trips = [d.trip for d in departures]
        positions = self.position_repository.find_all(system, trip=trips)
        return self.page(
            name='stop/overview',
            title=f'Stop {stop.number}',
            system=system,
            agency=agency,
            include_maps=True,
            stop=stop,
            departures=departures,
            recorded_today=self.record_repository.find_recorded_today(system, trips),
            assignments=self.assignment_repository.find_all(system, stop=stop),
            positions={p.trip.id: p for p in positions},
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def stop_map(self, system, agency, stop_number):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'stops/{stop_number}/map',
                system=system,
                agency=agency
            )
        stop = system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                name='invalid_stop',
                title='Unknown Stop',
                system=system,
                agency=agency,
                stop_number=stop_number
            )
        return self.page(
            name='stop/map',
            title=f'Stop {stop.number}',
            system=system,
            agency=agency,
            include_maps=True,
            full_map=True,
            stop=stop,
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def stop_schedule(self, system, agency, stop_number):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'stops/{stop_number}/schedule',
                system=system,
                agency=agency
            )
        stop = system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                name='invalid_stop',
                title='Unknown Stop',
                system=system,
                agency=agency,
                stop_number=stop_number
            )
        return self.page(
            name='stop/schedule',
            title=f'Stop {stop.number}',
            system=system,
            agency=agency,
            enable_refresh=False,
            stop=stop,
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def stop_schedule_date(self, system, agency, stop_number, date_string):
        if not system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=f'stops/{stop_number}/schedule',
                system=system,
                agency=agency
            )
        stop = system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                name='invalid_stop',
                title='Unknown Stop',
                system=system,
                agency=agency,
                stop_number=stop_number
            )
        date = Date.parse(date_string, system.timezone)
        return self.page(
            name='stop/date',
            title=f'Stop {stop.number}',
            system=system,
            agency=agency,
            enable_refresh=False,
            stop=stop,
            date=date,
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def about(self, system, agency):
        return self.page(
            name='about',
            title='About',
            path='about',
            system=system,
            agency=agency,
            enable_refresh=False
        )
    
    def guide(self, system, agency):
        return self.page(
            name='guide',
            title='Guide',
            path='guide',
            system=system,
            agency=agency,
            enable_refresh=False
        )

    def nearby(self, system, agency):
        return self.page(
            name='nearby',
            title='Nearby Stops',
            path='nearby',
            system=system,
            agency=agency,
            include_maps=True
        )
    
    def themes(self, system, agency):
        redirect(self.get_url(system, 'personalize'))
    
    def personalize(self, system, agency):
        theme_id = request.query.get('theme')
        if theme_id:
            self.set_cookie('theme', theme_id)
        time_format = request.query.get('time_format')
        if time_format:
            self.set_cookie('time_format', time_format)
        bus_marker_style = request.query.get('bus_marker_style')
        if bus_marker_style:
            self.set_cookie('bus_marker_style', bus_marker_style)
        themes = self.theme_repository.find_all()
        return self.page(
            name='personalize',
            title='Personalize',
            path='personalize',
            system=system,
            agency=agency,
            enable_refresh=False,
            themes=themes
        )
    
    def systems(self, system, agency):
        return self.page(
            name='systems',
            title='Systems',
            path=request.query.get('path', ''),
            system=system,
            agency=agency,
            enable_refresh=False
        )
    
    def admin(self, system, agency):
        return self.page(
            name='admin',
            title='Administration',
            path='admin',
            system=system,
            agency=agency,
            enable_refresh=False,
            disable_indexing=True
        )
    
    # =============================================================
    # Frames
    # =============================================================
    
    def frame_nearby(self, system, agency):
        if not system:
            response.status = 400
            return None
        stops = sorted(system.get_stops())
        lat = float(request.query.get('lat'))
        lon = float(request.query.get('lon'))
        return self.frame(
            name='nearby',
            system=system,
            agency=agency,
            stops=sorted([s for s in stops if s.is_near(lat, lon)])
        )
    
    # =============================================================
    # API endpoints
    # =============================================================
    
    def api_health_check(self, system, agency):
        return 'Online'
    
    def api_map(self, system, agency):
        time_format = request.get_cookie('time_format')
        if system:
            last_updated = system.get_last_updated(time_format)
        else:
            last_updated = self.realtime_service.get_last_updated(time_format)
        positions = sorted(self.position_repository.find_all(system, has_location=True), key=lambda p: p.lat)
        return {
            'positions': [p.get_json() for p in positions],
            'last_updated': last_updated
        }
    
    def api_shape(self, system, agency, shape_id):
        return {
            'points': [p.get_json() for p in self.point_repository.find_all(system, shape_id)]
        }
    
    def api_routes(self, system, agency):
        routes = self.route_repository.find_all(system)
        trips = sorted([t for r in routes for t in r.trips], key=lambda t: t.route, reverse=True)
        shape_ids = set()
        shape_trips = []
        for trip in trips:
            if trip.shape_id not in shape_ids:
                shape_ids.add(trip.shape_id)
                shape_trips.append(trip.get_json())
        indicators = [j for r in routes for j in r.get_indicator_json()]
        return {
            'trips': shape_trips,
            'indicators': sorted(indicators, key=lambda j: j['lat'])
        }
    
    def api_search(self, system, agency):
        query = request.forms.get('query', '')
        page = int(request.forms.get('page', 0))
        count = int(request.forms.get('count', 10))
        include_buses = int(request.forms.get('include_buses', 1)) == 1
        include_routes = int(request.forms.get('include_routes', 1)) == 1
        include_stops = int(request.forms.get('include_stops', 1)) == 1
        include_blocks = int(request.forms.get('include_blocks', 1)) == 1
        matches = []
        if query != '':
            if query.isnumeric() and (not system or system.realtime_enabled):
                if include_buses:
                    bus_numbers = self.overview_repository.find_bus_numbers(system)
                    matches += self.order_repository.find_matches(agency, query, bus_numbers)
            if system:
                if include_blocks:
                    matches += system.search_blocks(query)
                if include_routes:
                    matches += system.search_routes(query)
                if include_stops:
                    matches += system.search_stops(query)
        matches = sorted([m for m in matches if m.value > 0])
        min = page * count
        max = min + count
        return {
            'results': [m.get_json(system, self.get_url) for m in matches[min:max]],
            'total': len(matches)
        }
    
    def api_nearby(self, system, agency):
        if not system:
            return {
                'stops': []
            }
        lat = float(request.query.get('lat'))
        lon = float(request.query.get('lon'))
        stops = sorted([s for s in system.get_stops() if s.is_near(lat, lon)])
        return {
            'stops': [s.get_json() for s in stops]
        }
    
    def api_admin_reload_adornments(self, system, agency):
        self.adornment_repository.load()
        return 'Success'
    
    def api_admin_reload_orders(self, system, agency):
        self.order_repository.load()
        return 'Success'
    
    def api_admin_reload_systems(self, system, agency):
        self.cron_service.stop()
        self.position_repository.delete_all()
        self.system_repository.load()
        for system in self.system_repository.find_all():
            if self.running:
                self.gtfs_service.load(system)
                if not self.gtfs_service.validate(system):
                    self.gtfs_service.load(system, True)
                self.gtfs_service.update_cache_in_background(system)
                self.realtime_service.update(system)
                if not self.realtime_service.validate(system):
                    system.validation_errors += 1
        if self.running:
            self.realtime_service.update_records()
            self.cron_service.start()
        return 'Success'
    
    def api_admin_reload_themes(self, system, agency):
        self.theme_repository.load()
        return 'Success'
    
    def api_admin_restart_cron(self, system, agency):
        self.cron_service.stop()
        self.cron_service.start()
        return 'Success'
    
    def api_admin_backup_database(self, system, agency):
        self.database.archive()
        return 'Success'
    
    def api_admin_reload_gtfs(self, system, agency, reload_system_id):
        system = self.system_repository.find(reload_system_id)
        if not system:
            return 'Invalid system'
        self.gtfs_service.load(system, True)
        self.gtfs_service.update_cache_in_background(system)
        self.realtime_service.update(system)
        if not self.realtime_service.validate(system):
            system.validation_errors += 1
        self.realtime_service.update_records()
        return 'Success'
    
    def api_admin_reload_realtime(self, system, agency, reload_system_id):
        system = self.system_repository.find(reload_system_id)
        if not system:
            return 'Invalid system'
        self.realtime_service.update(system)
        if not self.realtime_service.validate(system):
            system.validation_errors += 1
        self.realtime_service.update_records()
        return 'Success'
    
    # =============================================================
    # Errors
    # =============================================================
    
    def error_403(self, error):
        return self.error_page(
            name='403', 
            title='Forbidden',
            system=None,
            agency=None,
            error=error
        )
    
    def error_404(self, error):
        return self.error_page(
            name='404',
            title='Not Found',
            system=None,
            agency=None,
            error=error
        )
    
    def error_500(self, error):
        return self.error_page(
            name='500',
            title='Internal Error',
            system=None,
            agency=None,
            error=error
        )
