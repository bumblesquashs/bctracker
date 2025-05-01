
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, HTTPError, static_file, template, request, response, debug, redirect
from datetime import timedelta
from random import Random
import cherrypy as cp

from di import di
from database import Database
from settings import Settings

from models.bus import Bus
from models.context import Context
from models.date import Date
from models.event import Event
from models.favourite import Favourite, FavouriteSet
from models.time import Time
from models.timestamp import Timestamp

from repositories import *
from services import *

# Increase the version to force CSS reload
VERSION = 54

random = Random()

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
        'stop_repository',
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
        self.stop_repository = kwargs.get('stop_repository') or di[StopRepository]
        self.system_repository = kwargs.get('system_repository') or di[SystemRepository]
        self.theme_repository = kwargs.get('theme_repository') or di[ThemeRepository]
        self.transfer_repository = kwargs.get('transfer_repository') or di[TransferRepository]
        
        self.cron_service = kwargs.get('cron_service') or di[CronService]
        self.gtfs_service = kwargs.get('gtfs_service') or di[GTFSService]
        self.realtime_service = kwargs.get('realtime_service') or di[RealtimeService]
        
        # Static files
        self.add('/style/<name:path>', append_slash=False, validate_system=False, callback=self.style)
        self.add('/img/<name:path>', append_slash=False, validate_system=False, callback=self.img)
        self.add('/js/<name:path>', append_slash=False, validate_system=False, callback=self.js)
        self.add('/robots.txt', append_slash=False, validate_system=False, callback=self.robots_text)
        
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
        self.add('/blocks', callback=self.blocks_overview)
        self.add('/blocks/schedule', callback=self.blocks_schedule)
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
        self.add('/nearby', callback=self.nearby)
        self.add('/themes', callback=self.themes)
        self.add('/personalize', callback=self.personalize)
        self.add('/systems', callback=self.systems)
        self.add('/random', callback=self.random)
        self.add('/admin', require_admin=True, callback=self.admin)
        
        # Frames
        self.add('/frame/nearby', append_slash=False, callback=self.frame_nearby)
        
        # API endpoints
        self.add('/api/health-check', append_slash=False, callback=self.api_health_check)
        self.add('/api/positions', append_slash=False, callback=self.api_positions)
        self.add('/api/shape/<shape_id>', append_slash=False, callback=self.api_shape)
        self.add('/api/stops', append_slash=False, callback=self.api_stops)
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
        
        self.position_repository.delete_all(Context())
        
        handler = TimedRotatingFileHandler(filename='logs/access_log.log', when='d', interval=7)
        log = WSGILogger(self, [handler], ApacheFormatter())
        
        cp.tree.graft(log, '/')
        cp.server.start()
        
        for system in self.system_repository.find_all():
            context = Context(system=system)
            if self.running:
                try:
                    self.gtfs_service.load(context, args.reload, args.updatedb)
                    if not self.gtfs_service.validate(context):
                        self.gtfs_service.load(context, True)
                    self.gtfs_service.update_cache(context)
                    self.realtime_service.update(context)
                except Exception as e:
                    print(f'Error loading data for {context}: {e}')
                if not system.gtfs_downloaded or not self.realtime_service.validate(context):
                    system.reload_backoff.increase_value()
        if self.running:
            try:
                self.realtime_service.update_records()
            except Exception as e:
                print(f'Error updating records: {e}')
            self.cron_service.start()
    
    def stop(self):
        '''Terminates the server'''
        self.running = False
        self.cron_service.stop()
        self.database.disconnect()
        if cp.server.running:
            cp.server.stop()
    
    def get_url(self, context, *args, **kwargs):
        '''Returns a URL formatted based on the given context and path'''
        components = []
        for arg in args:
            try:
                components.append(str(arg.url_id))
            except AttributeError:
                components.append(str(arg))
        path = '/'.join(components)
        if type(context) is Context:
            system_id = context.system_id
        else:
            system_id = getattr(context, 'id', context)
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
    
    def page(self, context: Context, name, title, path=None, path_args=None, enable_refresh=True, include_maps=False, full_map=False, **kwargs):
        '''Returns an HTML page with the given name and details'''
        is_admin = self.validate_admin()
        
        time_format = self.query_cookie('time_format')
        bus_marker_style = self.query_cookie('bus_marker_style')
        hide_systems = self.query_cookie('hide_systems') != 'no'
        if context.system:
            last_updated = context.system.last_updated
            today = Date.today(context.timezone)
            now = Time.now(context.timezone, False)
            timestamp = Timestamp.now(context.timezone)
        else:
            last_updated = self.realtime_service.get_last_updated()
            today = Date.today()
            now = Time.now()
            timestamp = Timestamp.now()
        theme_id = self.query_cookie('theme')
        theme = self.theme_repository.find(theme_id)
        if not theme:
            if today.month == 10 and today.day == 31:
                theme = self.theme_repository.find('halloween')
            elif today.month == 12 and today.day == 25:
                theme = self.theme_repository.find('christmas')
            else:
                theme = self.theme_repository.find('bc-transit')
        theme_variant = self.query_cookie('theme_variant')
        high_contrast = self.query_cookie('high_contrast') == 'enabled'
        return template(f'pages/{name}',
            di=di,
            settings=self.settings,
            version=VERSION,
            title=title,
            path=path or [],
            path_args=path_args or {},
            context=context,
            enable_refresh=enable_refresh,
            include_maps=include_maps or full_map,
            full_map=full_map,
            regions=self.region_repository.find_all(),
            systems=self.system_repository.find_all(),
            agencies=self.agency_repository.find_all(),
            is_admin=is_admin,
            get_url=self.get_url,
            last_updated=last_updated,
            theme=theme,
            theme_variant=theme_variant,
            high_contrast=high_contrast,
            time_format=time_format,
            bus_marker_style=bus_marker_style,
            hide_systems=hide_systems,
            show_speed=request.get_cookie('speed') == '1994',
            show_random=request.get_cookie('random') == 'kumquat',
            today=today,
            now=now,
            timestamp=timestamp,
            **kwargs
        )
    
    def error_page(self, context: Context, name, title, path=None, path_args=None, **kwargs):
        '''Returns an error page with the given name and details'''
        return self.page(
            context=context,
            name=f'errors/{name}',
            title=title,
            path=path or [],
            path_args=path_args or {},
            enable_refresh=False,
            **kwargs
        )
    
    def frame(self, name, context: Context, **kwargs):
        '''Returns an HTML element that can be inserted into a page'''
        return template(f'frames/{name}',
            context=context,
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
    
    def query_options(self, key, options):
        '''
        Returns the value of the given key from the query and validates that it's in the given options.
        If no value exists or it isn't in the options list, the first option is returned.
        '''
        value = request.query.get(key)
        if value and value in options:
            return value
        return options[0]
    
    def add(self, base_path, method='GET', append_slash=True, require_admin=False, system_key='system_id', validate_system=True, callback=None):
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
                if validate_system and not system:
                    raise HTTPError(404)
                del kwargs[system_key]
            else:
                system = None
            if system:
                agency = system.agency
            else:                
                agency = self.agency_repository.find('bc-transit')
            context = Context(agency, system)
            return callback(context=context, *args, **kwargs)
        self.route(paths, method, callback=endpoint)
    
    # =============================================================
    # Static Files
    # =============================================================
    
    def style(self, context: Context, name):
        return static_file(name, root='./style')
    
    def img(self, context: Context, name):
        return static_file(name, root='./img')
    
    def js(self, context: Context, name):
        return static_file(name, root='./js')
    
    def robots_text(self, context: Context):
        return static_file('robots.txt', root='.')
    
    # =============================================================
    # Pages
    # =============================================================
    
    def home(self, context: Context):
        return self.page(
            context=context,
            name='home',
            title='Home',
            enable_refresh=False,
            favourites=self.get_favourites()
        )
    
    def news(self, context: Context):
        return self.page(
            context=context,
            name='news',
            title='News Archive',
            path=['news'],
            enable_refresh=False
        )
    
    def map(self, context: Context):
        positions = self.position_repository.find_all(context, has_location=True)
        auto_refresh = self.query_cookie('auto_refresh', 'false') != 'false'
        show_route_lines = self.query_cookie('show_route_lines', 'false') != 'false'
        show_stops = self.query_cookie('show_stops', 'true') != 'false'
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        stop_area = self.stop_repository.find_area(context)
        return self.page(
            context=context,
            name='map',
            title='Map',
            path=['map'],
            full_map=True,
            positions=sorted(positions, key=lambda p: p.lat),
            auto_refresh=auto_refresh,
            show_route_lines=show_route_lines,
            show_stops=show_stops,
            show_nis=show_nis,
            stop_area=stop_area
        )
    
    def realtime_all(self, context: Context):
        positions = self.position_repository.find_all(context)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            context=context,
            name='realtime/all',
            title='Realtime',
            path=['realtime'],
            positions=positions,
            show_nis=show_nis
        )
    
    def realtime_routes(self, context: Context):
        positions = self.position_repository.find_all(context)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            context=context,
            name='realtime/routes',
            title='Realtime',
            path=['realtime', 'routes'],
            positions=positions,
            show_nis=show_nis
        )
    
    def realtime_models(self, context: Context):
        positions = self.position_repository.find_all(context)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            context=context,
            name='realtime/models',
            title='Realtime',
            path=['realtime', 'models'],
            positions=positions,
            show_nis=show_nis
        )
    
    def realtime_speed(self, context: Context):
        self.set_cookie('speed', '1994')
        positions = self.position_repository.find_all(context)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        return self.page(
            context=context,
            name='realtime/speed',
            title='Realtime',
            path=['realtime', 'speed'],
            positions=positions,
            show_nis=show_nis
        )
    
    def fleet(self, context: Context):
        orders = self.order_repository.find_all(context)
        overviews = self.overview_repository.find_all(Context())
        return self.page(
            context=context,
            name='fleet',
            title='Fleet',
            path=['fleet'],
            orders=[o for o in sorted(orders) if o.visible],
            overviews={o.bus.number: o for o in overviews}
        )
    
    def bus_overview(self, context: Context, bus_number):
        bus = Bus.find(context, bus_number)
        overview = self.overview_repository.find(bus)
        if (not bus.order and not overview) or not bus.visible:
            return self.error_page(
                context=context,
                name='invalid_bus',
                title='Unknown Bus',
                bus_number=bus_number
            )
        position = self.position_repository.find(bus)
        records = self.record_repository.find_all(Context(), bus=bus, limit=20)
        return self.page(
            context=context,
            name='bus/overview',
            title=f'Bus {bus}',
            include_maps=bool(position),
            bus=bus,
            position=position,
            records=records,
            overview=overview,
            favourite=Favourite('vehicle', bus),
            favourites=self.get_favourites()
        )
    
    def bus_map(self, context: Context, bus_number):
        bus = Bus.find(context, bus_number)
        overview = self.overview_repository.find(bus)
        if (not bus.order and not overview) or not bus.visible:
            return self.error_page(
                context=context,
                name='invalid_bus',
                title='Unknown Bus',
                bus_number=bus_number
            )
        position = self.position_repository.find(bus)
        return self.page(
            context=context,
            name='bus/map',
            title=f'Bus {bus}',
            full_map=bool(position),
            bus=bus,
            position=position,
            favourite=Favourite('vehicle', bus),
            favourites=self.get_favourites()
        )
    
    def bus_history(self, context: Context, bus_number):
        bus = Bus.find(context, bus_number)
        overview = self.overview_repository.find(bus)
        if (not bus.order and not overview) or not bus.visible:
            return self.error_page(
                context=context,
                name='invalid_bus',
                title='Unknown Bus',
                bus_number=bus_number
            )
        try:
            page = int(request.query['page'])
        except (KeyError, ValueError):
            page = 1
        items_per_page = 100
        total_items = self.record_repository.count(Context(), bus=bus)
        if page < 1:
            records = []
        else:
            records = self.record_repository.find_all(Context(), bus=bus, limit=items_per_page, page=page)
        transfers = self.transfer_repository.find_all(bus=bus)
        tracked_systems = set()
        events = []
        if overview:
            tracked_systems.add(overview.first_seen_system)
            tracked_systems.add(overview.last_seen_system)
            events.append(Event(overview.first_seen_date, 'First Seen'))
            if overview.first_record:
                events.append(Event(overview.first_record.date, 'First Tracked'))
            events.append(Event(overview.last_seen_date, 'Last Seen'))
            if overview.last_record:
                events.append(Event(overview.last_record.date, 'Last Tracked'))
            for transfer in transfers:
                tracked_systems.add(transfer.old_system)
                tracked_systems.add(transfer.new_system)
                events.append(Event(transfer.date, 'Transferred',  f'{transfer.old_system} to {transfer.new_system}'))
        return self.page(
            context=context,
            name='bus/history',
            title=f'Bus {bus}',
            bus=bus,
            records=records,
            overview=overview,
            tracked_systems=tracked_systems,
            events=events,
            favourite=Favourite('vehicle', bus),
            favourites=self.get_favourites(),
            page=page,
            items_per_page=items_per_page,
            total_items=total_items
        )
    
    def history_last_seen(self, context: Context):
        overviews = [o for o in self.overview_repository.find_all(context) if o.last_record and o.bus.visible]
        try:
            days = int(request.query['days'])
        except (KeyError, ValueError):
            days = None
        if days:
            date = Date.today(context.timezone) - timedelta(days=days)
            overviews = [o for o in overviews if o.last_record.date > date]
        return self.page(
            context=context,
            name='history/last_seen',
            title='Vehicle History',
            path=['history'],
            path_args={
                'days': days
            },
            overviews=sorted(overviews, key=lambda o: o.bus),
            days=days
        )
    
    def history_first_seen(self, context: Context):
        overviews = [o for o in self.overview_repository.find_all(context) if o.first_record and o.bus.visible]
        return self.page(
            context=context,
            name='history/first_seen',
            title='Vehicle History',
            path=['history', 'first-seen'],
            overviews=sorted(overviews, key=lambda o: (o.first_record.date, o.first_record.first_seen, o.bus), reverse=True)
        )
    
    def history_transfers(self, context: Context):
        filter = request.query.get('filter')
        if filter == 'from':
            transfers = self.transfer_repository.find_all(old_system=context.system)
        elif filter == 'to':
            transfers = self.transfer_repository.find_all(new_system=context.system)
        else:
            transfers = self.transfer_repository.find_all(old_system=context.system, new_system=context.system)
        return self.page(
            context=context,
            name='history/transfers',
            title='Vehicle History',
            path=['history', 'transfers'],
            transfers=[t for t in transfers if t.bus.visible],
            filter=filter
        )
    
    def routes_list(self, context: Context):
        return self.page(
            context=context,
            name='routes/list',
            title='Routes',
            path=['routes'],
            enable_refresh=False
        )
    
    def routes_map(self, context: Context):
        routes = self.route_repository.find_all(context)
        show_route_numbers = self.query_cookie('show_route_numbers', 'true') != 'false'
        return self.page(
            context=context,
            name='routes/map',
            title='Routes',
            path=['routes', 'map'],
            enable_refresh=False,
            full_map=len(routes) > 0,
            routes=routes,
            show_route_numbers=show_route_numbers
        )
    
    def route_overview(self, context: Context, route_number):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number]
            )
        if context.agency.prefer_route_id:
            route = context.system.get_route(route_id=route_number)
        else:
            route = context.system.get_route(number=route_number)
        if not route:
            return self.error_page(
                context=context,
                name='invalid_route',
                title='Unknown Route',
                route_number=route_number
            )
        trips = sorted(route.get_trips(date=Date.today(context.timezone)))
        return self.page(
            context=context,
            name='route/overview',
            title=str(route),
            include_maps=len(route.trips) > 0,
            route=route,
            trips=trips,
            recorded_today=self.record_repository.find_recorded_today(context, trips),
            assignments=self.assignment_repository.find_all(context, route=route),
            positions=self.position_repository.find_all(context, route=route),
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_map(self, context: Context, route_number):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number, 'map']
            )
        if context.agency.prefer_route_id:
            route = context.system.get_route(route_id=route_number)
        else:
            route = context.system.get_route(number=route_number)
        if not route:
            return self.error_page(
                context=context,
                name='invalid_route',
                title='Unknown Route',
                route_number=route_number
            )
        return self.page(
            context=context,
            name='route/map',
            title=str(route),
            full_map=len(route.trips) > 0,
            route=route,
            positions=self.position_repository.find_all(context, route=route),
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_schedule(self, context: Context, route_number):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number, 'schedule']
            )
        if context.agency.prefer_route_id:
            route = context.system.get_route(route_id=route_number)
        else:
            route = context.system.get_route(number=route_number)
        if not route:
            return self.error_page(
                name='invalid_route',
                title='Unknown Route',
                context=context,
                route_number=route_number
            )
        return self.page(
            context=context,
            name='route/schedule',
            title=str(route),
            enable_refresh=False,
            route=route,
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_schedule_date(self, context: Context, route_number, date_string):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number, 'schedule']
            )
        if context.agency.prefer_route_id:
            route = context.system.get_route(route_id=route_number)
        else:
            route = context.system.get_route(number=route_number)
        if not route:
            return self.error_page(
                context=context,
                name='invalid_route',
                title='Unknown Route',
                route_number=route_number
            )
        date = Date.parse(date_string, context.timezone)
        return self.page(
            context=context,
            name='route/date',
            title=str(route),
            enable_refresh=False,
            route=route,
            date=date,
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def blocks_overview(self, context: Context):
        if context.system and context.realtime_enabled:
            recorded_buses = self.record_repository.find_recorded_today_by_block(context)
        else:
            recorded_buses = {}
        return self.page(
            context=context,
            name='blocks/overview',
            title='Blocks',
            path=['blocks'],
            recorded_buses=recorded_buses
        )
    
    def blocks_schedule(self, context: Context):
        return self.page(
            context=context,
            name='blocks/schedule',
            title='Blocks',
            path=['blocks', 'schedule'],
            enable_refresh=False
        )
    
    def blocks_schedule_date(self, context: Context, date_string):
        date = Date.parse(date_string, context.timezone)
        return self.page(
            context=context,
            name='blocks/date',
            title='Blocks',
            path=[f'blocks', 'schedule', date_string],
            enable_reload=False,
            date=date
        )
    
    def block_overview(self, context: Context, block_id):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['blocks', block_id]
            )
        block = context.system.get_block(block_id)
        if not block:
            return self.error_page(
                context=context,
                name='invalid_block',
                title='Unknown Block',
                block_id=block_id
            )
        return self.page(
            context=context,
            name='block/overview',
            title=f'Block {block.id}',
            include_maps=True,
            block=block,
            positions=self.position_repository.find_all(context, block=block),
            assignment=self.assignment_repository.find(context, block)
        )
    
    def block_map(self, context: Context, block_id):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['blocks', block_id, 'map']
            )
        block = context.system.get_block(block_id)
        if not block:
            return self.error_page(
                context=context,
                name='invalid_block',
                title='Unknown Block',
                block_id=block_id
            )
        return self.page(
            context=context,
            name='block/map',
            title=f'Block {block.id}',
            full_map=True,
            block=block,
            positions=self.position_repository.find_all(context, block=block)
        )
    
    def block_history(self, context: Context, block_id):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['blocks', block_id, 'history']
            )
        block = context.system.get_block(block_id)
        if not block:
            return self.error_page(
                context=context,
                name='invalid_block',
                title='Unknown Block',
                block_id=block_id
            )
        records = self.record_repository.find_all(context, block=block)
        events = []
        if records:
            events.append(Event(records[0].date, 'Last Tracked'))
            events.append(Event(records[-1].date, 'First Tracked'))
        return self.page(
            context=context,
            name='block/history',
            title=f'Block {block.id}',
            block=block,
            records=records,
            events=events
        )
    
    def trip_overview(self, context: Context, trip_id):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['trips', trip_id]
            )
        trip = context.system.get_trip(trip_id)
        if not trip:
            return self.error_page(
                context=context,
                name='invalid_trip',
                title='Unknown Trip',
                trip_id=trip_id
            )
        return self.page(
            context=context,
            name='trip/overview',
            title=f'Trip {trip.id}',
            include_maps=True,
            trip=trip,
            positions=self.position_repository.find_all(context, trip=trip),
            assignment=self.assignment_repository.find(context, trip.block_id)
        )
    
    def trip_map(self, context: Context, trip_id):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['trips', trip_id, 'map']
            )
        trip = context.system.get_trip(trip_id)
        if not trip:
            return self.error_page(
                context=context,
                name='invalid_trip',
                title='Unknown Trip',
                trip_id=trip_id
            )
        return self.page(
            context=context,
            name='trip/map',
            title=f'Trip {trip.id}',
            full_map=True,
            trip=trip,
            positions=self.position_repository.find_all(context, trip=trip)
        )
    
    def trip_history(self, context: Context, trip_id):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['trips', trip_id, 'history']
            )
        trip = context.system.get_trip(trip_id)
        if not trip:
            return self.error_page(
                context=context,
                name='invalid_trip',
                title='Unknown Trip',
                trip_id=trip_id
            )
        records = self.record_repository.find_all(context, trip=trip)
        events = []
        if records:
            events.append(Event(records[0].date, 'Last Tracked'))
            events.append(Event(records[-1].date, 'First Tracked'))
        return self.page(
            context=context,
            name='trip/history',
            title=f'Trip {trip.id}',
            trip=trip,
            records=records,
            events=events
        )
    
    def stops(self, context: Context):
        path_args = {}
        search = request.query.get('search')
        if search:
            path_args['search'] = search
        routes_query = request.query.get('routes')
        if routes_query:
            routes_filter = [r for r in routes_query.split(',') if r]
        else:
            routes_filter = []
        sort = self.query_options('sort', ['name', 'number'])
        if sort == 'number' and not context.agency.show_stop_number:
            sort = 'name'
        if sort != 'name':
            path_args['sort'] = sort
        sort_order = self.query_options('sort_order', ['asc', 'desc'])
        if sort_order != 'asc':
            path_args['sort_order'] = sort_order
        try:
            page = int(request.query['page'])
        except (KeyError, ValueError):
            page = 1
        items_per_page = 100
        if context.system:
            stops = context.system.get_stops()
            if search:
                stops = [s for s in stops if search.lower() in s.name.lower()]
            for route_url_id in routes_filter:
                stops = [s for s in stops if route_url_id in {r.url_id for r in s.routes}]
            if sort == 'number':
                stops.sort(key=lambda s: s.key, reverse=sort_order == 'desc')
            elif sort == 'name':
                stops.sort(key=lambda s: s.name, reverse=sort_order == 'desc')
            total_items = len(stops)
            start_index = (page - 1) * items_per_page
            end_index = page * items_per_page
            if page < 1:
                stops = []
            else:
                stops = stops[start_index:end_index]
        else:
            stops = []
            total_items = 0
        return self.page(
            context=context,
            name='stops',
            title='Stops',
            path=['stops'],
            path_args=path_args,
            enable_refresh=False,
            stops=stops,
            search=search,
            routes_filter=routes_filter,
            sort=sort,
            sort_order=sort_order,
            page=page,
            items_per_page=items_per_page,
            total_items=total_items
        )
    
    def stop_overview(self, context: Context, stop_number):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['stops', stop_number]
            )
        if context.agency.prefer_stop_id:
            stop = context.system.get_stop(stop_id=stop_number)
        else:
            stop = context.system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                context=context,
                name='invalid_stop',
                title='Unknown Stop',
                stop_number=stop_number
            )
        departures = stop.find_departures(date=Date.today(context.timezone))
        trips = [d.trip for d in departures]
        positions = self.position_repository.find_all(context, trip=trips)
        return self.page(
            context=context,
            name='stop/overview',
            title=str(stop),
            include_maps=True,
            stop=stop,
            departures=departures,
            recorded_today=self.record_repository.find_recorded_today(context, trips),
            assignments=self.assignment_repository.find_all(context, stop=stop),
            positions={p.trip.id: p for p in positions},
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def stop_map(self, context: Context, stop_number):
        if not context.system:
            return self.error_page(
                name='system_required',
                title='System Required',
                path=['stops', stop_number, 'map'],
                context=context
            )
        if context.agency.prefer_stop_id:
            stop = context.system.get_stop(stop_id=stop_number)
        else:
            stop = context.system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                name='invalid_stop',
                title='Unknown Stop',
                context=context,
                stop_number=stop_number
            )
        return self.page(
            name='stop/map',
            title=str(stop),
            context=context,
            full_map=True,
            stop=stop,
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def stop_schedule(self, context: Context, stop_number):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['stops', stop_number, 'schedule']
            )
        if context.agency.prefer_stop_id:
            stop = context.system.get_stop(stop_id=stop_number)
        else:
            stop = context.system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                context=context,
                name='invalid_stop',
                title='Unknown Stop',
                stop_number=stop_number
            )
        return self.page(
            context=context,
            name='stop/schedule',
            title=str(stop),
            enable_refresh=False,
            stop=stop,
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def stop_schedule_date(self, context: Context, stop_number, date_string):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['stops', stop_number, 'schedule']
            )
        if context.agency.prefer_stop_id:
            stop = context.system.get_stop(stop_id=stop_number)
        else:
            stop = context.system.get_stop(number=stop_number)
        if not stop:
            return self.error_page(
                context=context,
                name='invalid_stop',
                title='Unknown Stop',
                stop_number=stop_number
            )
        date = Date.parse(date_string, context.timezone)
        return self.page(
            context=context,
            name='stop/date',
            title=str(stop),
            enable_refresh=False,
            stop=stop,
            date=date,
            favourite=Favourite('stop', stop),
            favourites=self.get_favourites()
        )
    
    def about(self, context: Context):
        return self.page(
            context=context,
            name='about',
            title='About',
            path=['about'],
            enable_refresh=False
        )
    
    def nearby(self, context: Context):
        return self.page(
            context=context,
            name='nearby',
            title='Nearby Stops',
            path=['nearby'],
            include_maps=True
        )
    
    def themes(self, context: Context):
        redirect(self.get_url(context, 'personalize'))
    
    def personalize(self, context: Context):
        themes = self.theme_repository.find_all()
        return self.page(
            context=context,
            name='personalize',
            title='Personalize',
            path=['personalize'],
            enable_refresh=False,
            themes=themes
        )
    
    def systems(self, context: Context):
        return self.page(
            context=context,
            name='systems',
            title='Systems',
            path=['systems'],
            enable_refresh=False
        )
    
    def random(self, context: Context):
        self.set_cookie('random', 'kumquat')
        systems = list(self.system_repository.find_all())
        system = random.choice(systems)
        options = ['route', 'stop', 'block', 'trip']
        if system.realtime_enabled:
            options.append('bus')
        selection = random.choice(options)
        match selection:
            case 'bus':
                overviews = system.get_overviews()
                if not overviews:
                    redirect(self.get_url(system))
                overview = random.choice(overviews)
                redirect(self.get_url(system, 'bus', overview.bus))
            case 'route':
                routes = system.get_routes()
                if not routes:
                    redirect(self.get_url(system))
                route = random.choice(routes)
                redirect(self.get_url(system, 'routes', route))
            case 'stop':
                stops = system.get_stops()
                if not stops:
                    redirect(self.get_url(system))
                stop = random.choice(stops)
                redirect(self.get_url(system, 'stops', stop))
            case 'block':
                blocks = system.get_blocks()
                if not blocks:
                    redirect(self.get_url(system))
                block = random.choice(blocks)
                redirect(self.get_url(system, 'blocks', block))
            case 'trip':
                trips = list(system.get_trips())
                if not trips:
                    redirect(self.get_url(system))
                trip = random.choice(trips)
                redirect(self.get_url(system, 'trips', trip))
    
    def admin(self, context: Context):
        return self.page(
            context=context,
            name='admin',
            title='Administration',
            path=['admin'],
            enable_refresh=False,
            disable_indexing=True
        )
    
    # =============================================================
    # Frames
    # =============================================================
    
    def frame_nearby(self, context: Context):
        if not context.system:
            response.status = 400
            return None
        stops = sorted(context.system.get_stops())
        lat = float(request.query.get('lat'))
        lon = float(request.query.get('lon'))
        return self.frame(
            context=context,
            name='nearby',
            stops=sorted([s for s in stops if s.is_near(lat, lon)])
        )
    
    # =============================================================
    # API endpoints
    # =============================================================
    
    def api_health_check(self, context: Context):
        return 'Online'
    
    def api_positions(self, context: Context):
        if context.system:
            last_updated = context.system.last_updated
        else:
            last_updated = self.realtime_service.get_last_updated()
        if last_updated:
            time_format = request.get_cookie('time_format')
            last_updated_text = last_updated.format_web(time_format)
        else:
            last_updated_text = None
        positions = sorted(self.position_repository.find_all(context, has_location=True), key=lambda p: p.lat)
        return {
            'positions': [p.get_json() for p in positions],
            'last_updated': last_updated_text
        }
    
    def api_shape(self, context: Context, shape_id):
        return {
            'points': [p.get_json() for p in self.point_repository.find_all(context, shape_id)]
        }
    
    def api_stops(self, context: Context):
        lat = float(request.query['lat'])
        lon = float(request.query['lon'])
        size = float(request.query.get('size', 0.01))
        stops = self.stop_repository.find_all(context, lat=lat, lon=lon, size=size)
        return {
            'stops': [s.get_json() for s in sorted(stops, key=lambda s: s.lat)]
        }
    
    def api_routes(self, context: Context):
        routes = self.route_repository.find_all(context)
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
    
    def api_search(self, context: Context):
        query = request.forms.get('query', '')
        page = int(request.forms.get('page', 0))
        count = int(request.forms.get('count', 10))
        include_buses = int(request.forms.get('include_buses', 1)) == 1
        include_routes = int(request.forms.get('include_routes', 1)) == 1
        include_stops = int(request.forms.get('include_stops', 1)) == 1
        include_blocks = int(request.forms.get('include_blocks', 1)) == 1
        matches = []
        if query != '':
            if query.isnumeric() and context.realtime_enabled:
                if include_buses:
                    bus_numbers = self.overview_repository.find_bus_numbers(context)
                    matches += self.order_repository.find_matches(context, query, bus_numbers)
            if context.system:
                if include_blocks:
                    matches += context.system.search_blocks(query)
                if include_routes:
                    matches += context.system.search_routes(query)
                if include_stops:
                    matches += context.system.search_stops(query)
        matches = sorted([m for m in matches if m.value > 0])
        min = page * count
        max = min + count
        return {
            'results': [m.get_json(context, self.get_url) for m in matches[min:max]],
            'total': len(matches)
        }
    
    def api_nearby(self, context: Context):
        if not context.system:
            return {
                'stops': []
            }
        lat = float(request.query.get('lat'))
        lon = float(request.query.get('lon'))
        stops = sorted([s for s in context.system.get_stops() if s.is_near(lat, lon)])
        return {
            'stops': [s.get_json() for s in stops]
        }
    
    def api_admin_reload_adornments(self, context: Context):
        self.adornment_repository.load()
        return 'Success'
    
    def api_admin_reload_orders(self, context: Context):
        self.order_repository.load()
        return 'Success'
    
    def api_admin_reload_systems(self, context: Context):
        self.cron_service.stop()
        self.position_repository.delete_all(Context())
        self.system_repository.load()
        for system in self.system_repository.find_all():
            if self.running:
                try:
                    self.gtfs_service.load(system)
                    if not self.gtfs_service.validate(system):
                        self.gtfs_service.load(system, True)
                    self.gtfs_service.update_cache(system)
                    self.realtime_service.update(system)
                except Exception as e:
                    print(f'Error loading data for {system}: {e}')
                if not system.gtfs_downloaded or not self.realtime_service.validate(system):
                    system.reload_backoff.increase_value()
        if self.running:
            try:
                self.realtime_service.update_records()
            except Exception as e:
                print(f'Error updating records: {e}')
            self.cron_service.start()
        return 'Success'
    
    def api_admin_reload_themes(self, context: Context):
        self.theme_repository.load()
        return 'Success'
    
    def api_admin_restart_cron(self, context: Context):
        self.cron_service.stop()
        self.cron_service.start()
        return 'Success'
    
    def api_admin_backup_database(self, context: Context):
        self.database.archive()
        return 'Success'
    
    def api_admin_reload_gtfs(self, context: Context, reload_system_id):
        system = self.system_repository.find(reload_system_id)
        if not system:
            return 'Invalid system'
        try:
            self.gtfs_service.load(system, True)
            self.gtfs_service.update_cache(system)
            self.realtime_service.update(system)
            self.realtime_service.update_records()
            if not system.gtfs_downloaded or not self.realtime_service.validate(system):
                system.reload_backoff.increase_value()
            return 'Success'
        except Exception as e:
            print(f'Error loading GTFS data for {system}: {e}')
            return str(e)
    
    def api_admin_reload_realtime(self, context: Context, reload_system_id):
        system = self.system_repository.find(reload_system_id)
        if not system:
            return 'Invalid system'
        try:
            self.realtime_service.update(system)
            self.realtime_service.update_records()
            if not self.realtime_service.validate(system):
                system.reload_backoff.increase_value()
            return 'Success'
        except Exception as e:
            print(f'Error loading realtime data for {system}: {e}')
            return str(e)
    
    # =============================================================
    # Errors
    # =============================================================
    
    def error_403(self, error):
        return self.error_page(
            context=Context(),
            name='403', 
            title='Forbidden',
            error=error
        )
    
    def error_404(self, error):
        return self.error_page(
            context=Context(),
            name='404',
            title='Not Found',
            error=error
        )
    
    def error_500(self, error):
        return self.error_page(
            context=Context(),
            name='500',
            title='Internal Error',
            error=error
        )
