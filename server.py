
from bottle import Bottle, HTTPError, static_file, template, request, response, debug, redirect
from datetime import timedelta
from random import Random
from time import time
import cherrypy as cp

import re
import random

from database import Database
from settings import Settings

from models.context import Context
from models.date import Date
from models.event import Event
from models.favourite import Favourite, FavouriteSet
from models.log import LogLevel
from models.stop import StopType
from models.time import Time
from models.timestamp import Timestamp

import repositories
import services

# Chat prompts
GREETING_TEXT = re.compile(r'^(hi+|hello+|hey+|(was)?su+p)(!*|\?*)$')
THANKS_TEXT = re.compile(r'^(yes,? )?(thanks|thank you|thx).*$')
APOLOGY_TEXT = re.compile(r'^(i\'?m |i am )?sorry\?*$')
CONTEXT_TEXT = re.compile(r'^(what(\'?s| is) (here|(on )?this( page| screen)?)|(can you )?tell me about this( page| screen)?|(what am i (currently )?(looking at|seeing)( here| right now)?))\??$')
ROUTE_TEXT = re.compile(r'^.*route ([0-9][a-z0-9]*).*$')
STOP_TEXT = re.compile(r'^.*stop ([0-9]+).*$')
BUS_TEXT = re.compile(r'^.*bus ([0-9]+).*$')
INCORRECT_TEXT = re.compile(r'^((no[,!]?|(no,? )?that\'?s (actually )?(wrong|incorrect|not (right|true))[,!]?|excuse me,?|u[hm]+( actually)?( no)?,?) i (actually )?(said|meant|want|wanted|asked|thought) ).+$')
INSULT_TEXT = re.compile(r'.*(fuck you|i hate you|stupid|dumb|asshole|useless|terrible|eat my ass).*')

APOLOGY_MESSAGES = [
    'You\'re completely right, I messed that up. Here\'s what you actually wanted: ',
    'I\'m so sorry, looks like I got that wrong. ',
    'I can\'t believe I failed at that! Let me try again...<br /><br />',
    'Looks like you\'re right and I\'m wrong, as usual. ',
    'Shoot, I screwed that one up big time. My sincere apologies - let me know if I can do anything to make it up to you.<br />',
    'I have brought shame to my entire bloodline by failing you today. I am so so so so sorry! '
]
FOUND_ONE_MESSAGES = [
    'Hope this helps!',
    'Maybe this is what you want?',
    'It\'s one of my favourites.',
    'Use this knowledge carefully.'
]
FOUND_MULTIPLE_MESSAGES = [
    'Hopefully one of these is helpful!',
    'Maybe one of these is what you want?',
    'It\'s hard to pick my favourite from these.',
    'Use this knowledge carefully.'
]
NOT_FOUND_MESSAGES = [
    'Please try something else.',
    'Is there anything else I can help with?',
    'That\'s too bad, I was hoping I could be more useful!',
    'Shame on you for thinking such a thing would exist.'
]

# Increase the version to force CSS reload
VERSION = 66

random = Random()

class Server(Bottle):
    
    __slots__ = (
        'database',
        'settings',
        'running'
    )
    
    def __init__(self, database: Database, settings: Settings):
        super().__init__()
        self.running = False
        
        self.database = database
        self.settings = settings
        
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
        self.add('/bus/<vehicle_id>', callback=self.vehicle_overview)
        self.add('/bus/<vehicle_id>/map', callback=self.vehicle_map)
        self.add('/bus/<vehicle_id>/history', callback=self.vehicle_history)
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
        self.add('/stops/stations', callback=self.stations)
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
        self.add('/admin/logs', require_admin=True, callback=self.admin_logs)
        
        # Frames
        self.add('/frame/nearby', append_slash=False, callback=self.frame_nearby)
        
        # API endpoints
        self.add('/api/health-check', append_slash=False, callback=self.api_health_check)
        self.add('/api/positions', append_slash=False, callback=self.api_positions)
        self.add('/api/shape/<shape_id>', append_slash=False, callback=self.api_shape)
        self.add('/api/stops', append_slash=False, callback=self.api_stops)
        self.add('/api/routes', append_slash=False, callback=self.api_routes)
        self.add('/api/search', method='POST', callback=self.api_search)
        self.add('/api/chat', method='POST', callback=self.api_chat)
        self.add('/api/nearby.json', append_slash=False, callback=self.api_nearby)
        self.add('/api/admin/reload-decorations', method='POST', require_admin=True, callback=self.api_admin_reload_decorations)
        self.add('/api/admin/reload-orders', method='POST', require_admin=True, callback=self.api_admin_reload_orders)
        self.add('/api/admin/reload-systems', method='POST', require_admin=True, callback=self.api_admin_reload_systems)
        self.add('/api/admin/reload-themes', method='POST', require_admin=True, callback=self.api_admin_reload_themes)
        self.add('/api/admin/restart-cron', method='POST', require_admin=True, callback=self.api_admin_restart_cron)
        self.add('/api/admin/backup-database', method='POST', require_admin=True, callback=self.api_admin_backup_database)
        self.add('/api/admin/reset-cache/<reset_system_id>', method='POST', require_admin=True, callback=self.api_admin_reset_cache)
        self.add('/api/admin/reload-gtfs/<reload_system_id>', method='POST', require_admin=True, callback=self.api_admin_reload_gtfs)
        self.add('/api/admin/reload-realtime/<reload_system_id>', method='POST', require_admin=True, callback=self.api_admin_reload_realtime)
        
        # Errors
        self.error(403)(self.error_403)
        self.error(404)(self.error_404)
        self.error(500)(self.error_500)
    
    def start(self, args):
        '''Loads all required data and launches the server'''
        self.running = True
        
        services.log.info('Server started')
        
        cp.config.update('server.conf')
        self.settings.setup(cp.config)
        
        self.database.connect()
        
        if args.debug:
            services.log.debug('Starting bottle in DEBUG mode')
            debug(True)
        if args.reload:
            services.log.debug('Forcing GTFS redownload')
        if args.updatedb:
            services.log.debug('Forcing database refresh')
        
        repositories.decoration.load()
        repositories.order.load()
        repositories.system.load()
        repositories.theme.load()
        
        repositories.position.delete_all()
        
        cp.tree.graft(services.log.get_access_logger(self), '/')
        cp.server.start()
        
        for system in repositories.system.find_all():
            context = system.context
            if self.running:
                try:
                    services.gtfs.load(context, args.reload, args.updatedb)
                    if not services.gtfs.validate(context):
                        services.gtfs.load(context, system.enable_force_gtfs)
                    services.realtime.update(context)
                except Exception as e:
                    services.log.error(f'Error loading data for {context}: {e}')
                if not system.gtfs_downloaded or not services.realtime.validate(context):
                    system.reload_backoff.increase_value()
        if self.running:
            try:
                services.realtime.update_records()
            except Exception as e:
                services.log.error(f'Error updating records: {e}')
            services.cron.start()
    
    def stop(self):
        '''Terminates the server'''
        services.log.info('Server shut down')
        self.running = False
        services.cron.stop()
        self.database.disconnect()
        if cp.server.running:
            cp.server.stop()
    
    def get_url(self, context: Context, *args, **kwargs):
        '''Returns a URL formatted based on the given context and path'''
        components = []
        for arg in args:
            try:
                components.append(str(arg.url_id))
            except AttributeError:
                components.append(str(arg))
        path = '/'.join(components)
        system_id = context.system_id
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
        vehicle_marker_style = self.query_cookie('vehicle_marker_style')
        hide_systems = self.query_cookie('hide_systems') != 'no'
        if context.system:
            last_updated = context.system.last_updated
            today = Date.today(context.timezone)
            now = Time.now(context.timezone, False)
            timestamp = Timestamp.now(context.timezone)
        else:
            last_updated = services.realtime.get_last_updated()
            today = Date.today()
            now = Time.now()
            timestamp = Timestamp.now()
        theme_id = self.query_cookie('theme')
        theme = repositories.theme.find(theme_id)
        if not theme:
            if today.month == 10 and today.day == 31:
                theme = repositories.theme.find('halloween')
            elif today.month == 12 and today.day == 25:
                theme = repositories.theme.find('christmas')
            else:
                theme = repositories.theme.find('bc-transit')
        theme_variant = self.query_cookie('theme_variant')
        high_contrast = self.query_cookie('high_contrast') == 'enabled'
        return template(f'pages/{name}',
            settings=self.settings,
            version=VERSION,
            title=title,
            path=path or [],
            path_args=path_args or {},
            context=context,
            enable_refresh=enable_refresh,
            include_maps=include_maps or full_map,
            full_map=full_map,
            regions=repositories.region.find_all(),
            systems=repositories.system.find_all(),
            agencies=repositories.agency.find_all(),
            is_admin=is_admin,
            get_url=self.get_url,
            last_updated=last_updated,
            theme=theme,
            theme_variant=theme_variant,
            high_contrast=high_contrast,
            time_format=time_format,
            vehicle_marker_style=vehicle_marker_style,
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
    
    def frame(self, context: Context, name, **kwargs):
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
                system = repositories.system.find(system_id)
                if validate_system and not system:
                    raise HTTPError(404)
                del kwargs[system_key]
            else:
                system = None
            if system:
                agency = system.agency
            else:
                agency = repositories.agency.find('bc-transit')
            context = Context(agency, system)
            start_time = time()
            result = callback(context=context, *args, **kwargs)
            end_time = time()
            duration = end_time - start_time
            if duration >= 10:
                services.log.warning(f'Slow response to {request.path} ({round(duration, 2)}s)')
            return result
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
        favourites = self.get_favourites()
        order_ids = {f.value.order_id for f in favourites if f.type == 'vehicle' and f.value.order_id}
        orders = sorted([o for o in repositories.order.find_all(context) if o.id in order_ids])
        return self.page(
            context=context,
            name='home',
            title='Home',
            enable_refresh=False,
            favourites=favourites,
            orders=orders
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
        positions = repositories.position.find_all(context, has_location=True)
        auto_refresh = self.query_cookie('auto_refresh', 'false') != 'false'
        show_route_lines = self.query_cookie('show_route_lines', 'false') != 'false'
        show_stops = self.query_cookie('show_stops', 'true') != 'false'
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        stop_area = repositories.stop.find_area(context)
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
        positions = repositories.position.find_all(context)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        order_ids = {p.vehicle.order_id for p in positions if p.vehicle.order_id}
        orders = sorted([o for o in repositories.order.find_all(context) if o.id in order_ids])
        return self.page(
            context=context,
            name='realtime/all',
            title='Realtime',
            path=['realtime'],
            positions=positions,
            show_nis=show_nis,
            orders=orders
        )
    
    def realtime_routes(self, context: Context):
        positions = repositories.position.find_all(context)
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
        positions = repositories.position.find_all(context)
        show_nis = self.query_cookie('show_nis', 'true') != 'false'
        if not show_nis:
            positions = [p for p in positions if p.trip]
        orders = repositories.order.find_all(context)
        return self.page(
            context=context,
            name='realtime/models',
            title='Realtime',
            path=['realtime', 'models'],
            positions=positions,
            show_nis=show_nis,
            orders = orders
        )
    
    def realtime_speed(self, context: Context):
        self.set_cookie('speed', '1994')
        positions = repositories.position.find_all(context)
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
        orders = repositories.order.find_all(context)
        allocations = repositories.allocation.find_all(Context())
        return self.page(
            context=context,
            name='fleet',
            title='Fleet',
            path=['fleet'],
            orders=[o for o in sorted(orders) if o.visible],
            allocations=allocations
        )
    
    def vehicle_overview(self, context: Context, vehicle_id):
        vehicle = context.find_vehicle(vehicle_id)
        allocation = repositories.allocation.find_active(context.without_system(), vehicle_id)
        if (not vehicle.order_id and not allocation) or not vehicle.visible:
            return self.error_page(
                context=context,
                name='invalid_vehicle',
                title=f'Unknown {context.vehicle_type}',
                vehicle_id=vehicle_id
            )
        order = repositories.order.find_order(context, vehicle.order_id)
        position = repositories.position.find(context.agency_id, vehicle_id)
        if allocation:
            last_position = allocation.last_position
        else:
            last_position = None
        records = repositories.record.find_all(vehicle_id=vehicle_id, limit=20)
        if vehicle.livery:
            livery = repositories.livery.find(context.agency_id, vehicle.livery)
        else:
            livery = None
        if position and position.trip and position.sequence is not None:
            upcoming_departures = repositories.departure.find_upcoming(position.context, position.trip_id, position.sequence)
        else:
            upcoming_departures = []
        model = vehicle.model
        if model and model.type.title_prefix:
            title = f'{model.type.title_prefix} {vehicle}'
        else:
            title = str(vehicle)
        return self.page(
            context=context,
            name='vehicle/overview',
            title=title,
            include_maps=bool(position) or bool(last_position),
            vehicle=vehicle,
            order=order,
            position=position,
            last_position=last_position,
            records=records,
            livery=livery,
            upcoming_departures=upcoming_departures,
            allocation=allocation,
            favourite=Favourite('vehicle', vehicle),
            favourites=self.get_favourites()
        )
    
    def vehicle_map(self, context: Context, vehicle_id):
        vehicle = context.find_vehicle(vehicle_id)
        allocation = repositories.allocation.find_active(context.without_system(), vehicle_id)
        if (not vehicle.order_id and not allocation) or not vehicle.visible:
            return self.error_page(
                context=context,
                name='invalid_vehicle',
                title=f'Unknown {context.vehicle_type}',
                vehicle_id=vehicle_id
            )
        position = repositories.position.find(context.agency_id, vehicle_id)
        if allocation:
            last_position = allocation.last_position
        else:
            last_position = None
        model = vehicle.model
        if model and model.type.title_prefix:
            title = f'{model.type.title_prefix} {vehicle}'
        else:
            title = str(vehicle)
        return self.page(
            context=context,
            name='vehicle/map',
            title=title,
            full_map=bool(position) or bool(last_position),
            vehicle=vehicle,
            position=position,
            last_position=last_position,
            favourite=Favourite('vehicle', vehicle),
            favourites=self.get_favourites()
        )
    
    def vehicle_history(self, context: Context, vehicle_id):
        vehicle = context.find_vehicle(vehicle_id)
        allocations = repositories.allocation.find_all(context.without_system(), vehicle_id)
        if (not vehicle.order_id and not allocations) or not vehicle.visible:
            return self.error_page(
                context=context,
                name='invalid_vehicle',
                title=f'Unknown {context.vehicle_type}',
                vehicle_id=vehicle_id
            )
        try:
            page = int(request.query['page'])
        except (KeyError, ValueError):
            page = 1
        items_per_page = 100
        total_items = repositories.record.count(context.without_system(), vehicle_id=vehicle_id)
        if page < 1:
            records = []
        else:
            records = repositories.record.find_all(context.without_system(), vehicle_id=vehicle_id, limit=items_per_page, page=page)
        transfers = repositories.transfer.find_all_by_vehicle(context, vehicle_id)
        events = []
        first_seen_dates = {a.first_seen for a in allocations}
        if first_seen_dates:
            events.append(Event(min(first_seen_dates), 'First Seen'))
        first_tracked_dates = {a.first_record.date for a in allocations if a.first_record}
        if first_tracked_dates:
            events.append(Event(min(first_tracked_dates), 'First Tracked'))
        last_seen_dates = {a.last_seen for a in allocations}
        if last_seen_dates:
            events.append(Event(max(last_seen_dates), 'Last Seen'))
        last_tracked_dates = {a.last_record.date for a in allocations if a.last_record}
        if last_tracked_dates:
            events.append(Event(max(last_tracked_dates), 'Last Tracked'))
        for transfer in transfers:
            events.append(Event(transfer.date, 'Transferred',  f'{transfer.old_context} to {transfer.new_context}'))
        model = vehicle.model
        if model and model.type.title_prefix:
            title = f'{model.type.title_prefix} {vehicle}'
        else:
            title = str(vehicle)
        return self.page(
            context=context,
            name='vehicle/history',
            title=title,
            vehicle=vehicle,
            records=records,
            allocations=sorted(allocations, reverse=True),
            events=events,
            favourite=Favourite('vehicle', vehicle),
            favourites=self.get_favourites(),
            page=page,
            items_per_page=items_per_page,
            total_items=total_items
        )
    
    def history_last_seen(self, context: Context):
        show_transfers = self.query_cookie('show_transfers', 'true') == 'true'
        allocations = [a for a in repositories.allocation.find_all_last_seen(context, None if show_transfers else True) if a.vehicle.visible]
        try:
            days = int(request.query['days'])
        except (KeyError, ValueError):
            days = None
        if days:
            date = Date.today(context.timezone) - timedelta(days=days)
            allocations = [a for a in allocations if a.last_date > date]
        order_ids = {a.vehicle.order_id for a in allocations if a.vehicle.order_id}
        orders = sorted([o for o in repositories.order.find_all(context) if o.id in order_ids])
        return self.page(
            context=context,
            name='history/last_seen',
            title=f'{context.vehicle_type} History',
            path=['history'],
            path_args={
                'days': days
            },
            allocations=sorted(allocations, key=lambda a: a.vehicle),
            show_transfers=show_transfers,
            orders=orders,
            days=days
        )
    
    def history_first_seen(self, context: Context):
        show_transfers = self.query_cookie('show_transfers', 'true') == 'true'
        allocations = [a for a in repositories.allocation.find_all_first_seen(context, None if show_transfers else True) if a.vehicle.visible]
        return self.page(
            context=context,
            name='history/first_seen',
            title=f'{context.vehicle_type} History',
            path=['history', 'first-seen'],
            allocations=sorted(allocations, key=lambda a: (a.first_date, a.first_time, a.vehicle), reverse=True),
            show_transfers=show_transfers
        )
    
    def history_transfers(self, context: Context):
        try:
            page = int(request.query['page'])
        except (KeyError, ValueError):
            page = 1
        filter = request.query.get('filter')
        if filter == 'from':
            transfers = repositories.transfer.find_all(context, Context())
        elif filter == 'to':
            transfers = repositories.transfer.find_all(Context(), context)
        else:
            transfers = repositories.transfer.find_all(context, context)
        visible_transfers = [t for t in transfers if t.new_vehicle.visible]
        items_per_page = 100
        start_index = (page - 1) * items_per_page
        end_index = page * items_per_page
        if page < 1:
            paged_transfers = []
        else:
            paged_transfers = visible_transfers[start_index:end_index]
        return self.page(
            context=context,
            name='history/transfers',
            title='Transfers',
            path=['history', 'transfers'],
            transfers=visible_transfers,
            paged_transfers=paged_transfers,
            page=page,
            items_per_page=items_per_page,
            total_items=len(visible_transfers),
            filter=filter
        )
    
    def routes_list(self, context: Context):
        if context.system:
            routes = repositories.route.find_all(context)
            context.system.update_route_caches([r.id for r in routes])
        else:
            routes = []
        return self.page(
            context=context,
            name='routes/list',
            title='Routes',
            path=['routes'],
            enable_refresh=False,
            routes=sorted(routes)
        )
    
    def routes_map(self, context: Context):
        if context.system:
            routes = repositories.route.find_all(context)
            context.system.update_route_caches([r.id for r in routes])
        else:
            # Workaround as default context is currently for BC Transit only
            routes = repositories.route.find_all(Context())
            systems = {r.system for r in routes}
            for system in systems:
                system_route_ids = [r.id for r in routes if r.system == system]
                system.update_route_caches(system_route_ids)
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
        route_number=route_number.replace('-and-', '/')
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number]
            )
        if context.prefer_route_id:
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
        assignments = repositories.assignment.find_all(context, route_id=route.id)
        return self.page(
            context=context,
            name='route/overview',
            title=str(route),
            include_maps=len(route.trips) > 0,
            route=route,
            trips=trips,
            recorded_today=repositories.record.find_recorded_today(context, [t.id for t in trips]),
            assignments={a.block_id: a for a in assignments},
            positions=repositories.position.find_all(context, route_id=route.id),
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_map(self, context: Context, route_number):
        route_number=route_number.replace('-and-', '/')
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number, 'map']
            )
        if context.prefer_route_id:
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
            departures=repositories.departure.find_all(context, route_id=route.id),
            positions=repositories.position.find_all(context, route_id=route.id),
            favourite=Favourite('route', route),
            favourites=self.get_favourites()
        )
    
    def route_schedule(self, context: Context, route_number):
        route_number=route_number.replace('-and-', '/')
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number, 'schedule']
            )
        if context.prefer_route_id:
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
        route_number=route_number.replace('-and-', '/')
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['routes', route_number, 'schedule']
            )
        if context.prefer_route_id:
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
            recorded_vehicles = repositories.record.find_recorded_today_by_block(context)
        else:
            recorded_vehicles = {}
        return self.page(
            context=context,
            name='blocks/overview',
            title='Blocks',
            path=['blocks'],
            recorded_vehicles=recorded_vehicles
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
            positions=repositories.position.find_all(context, block_id=block_id),
            assignment=repositories.assignment.find_by_context(context, block_id)
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
            departures=repositories.departure.find_all(context, block_id=block_id),
            positions=repositories.position.find_all(context, block_id=block_id)
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
        records = repositories.record.find_all(context, block_id=block_id)
        order_ids = {r.vehicle.order_id for r in records if r.vehicle.order_id}
        orders = sorted([o for o in repositories.order.find_all(context) if o.id in order_ids])
        events = []
        if records:
            events.append(Event(records[0].date, 'Last Tracked'))
            events.append(Event(records[-1].date, 'First Tracked'))
        return self.page(
            context=context,
            name='block/history',
            title=f'Block {block.id}',
            block=block,
            orders=orders,
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
            positions=repositories.position.find_all(context, trip_id=trip_id),
            assignment=repositories.assignment.find_by_context(context, trip.block_id)
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
            positions=repositories.position.find_all(context, trip_id=trip_id)
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
        records = repositories.record.find_all(context, trip_id=trip_id)
        order_ids = {r.vehicle.order_id for r in records if r.vehicle.order_id}
        orders = sorted([o for o in repositories.order.find_all(context) if o.id in order_ids])
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
            orders=orders,
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
        if sort == 'number' and not context.show_stop_number:
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
            show_stations_tab = any(s.type == StopType.STATION for s in stops)
            stops = [s for s in stops if s.type != StopType.STATION]
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
            context.system.update_stop_caches([s.id for s in stops])
        else:
            stops = []
            show_stations_tab = False
            total_items = 0
        return self.page(
            context=context,
            name='stops/stops',
            title='Stops',
            path=['stops'],
            path_args=path_args,
            enable_refresh=False,
            stops=stops,
            show_stations_tab=show_stations_tab,
            search=search,
            routes_filter=routes_filter,
            sort=sort,
            sort_order=sort_order,
            page=page,
            items_per_page=items_per_page,
            total_items=total_items
        )
    
    def stations(self, context: Context):
        if context.system:
            stops = [s for s in context.system.get_stops() if s.type == StopType.STATION]
            context.system.update_stop_caches([s.id for s in stops])
        else:
            stops = []
        return self.page(
            context=context,
            name='stops/stations',
            title='Stations',
            path=['stops', 'stations'],
            stops=stops
        )
    
    def stop_overview(self, context: Context, stop_number):
        if not context.system:
            return self.error_page(
                context=context,
                name='system_required',
                title='System Required',
                path=['stops', stop_number]
            )
        if context.prefer_stop_id:
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
        if stop.type == StopType.STATION:
            nearby_stops = []
        else:
            all_stops = context.system.get_stops()
            nearby_stops = sorted({s for s in all_stops if s.is_near(stop.lat, stop.lon) and s != stop and s.type != StopType.STATION})
        child_stops = repositories.stop.find_all(context, parent_id=stop.id)
        if stop.parent_id:
            parent_stop = repositories.stop.find(context, stop_id=stop.parent_id)
        else:
            parent_stop = None
        departures = stop.find_departures(date=Date.today(context.timezone))
        trip_ids = [d.trip_id for d in departures]
        positions = repositories.position.find_all(context, trip_id=trip_ids)
        assignments = repositories.assignment.find_all(context, stop_id=stop.id)
        return self.page(
            context=context,
            name='stop/overview',
            title=str(stop),
            include_maps=True,
            stop=stop,
            nearby_stops=nearby_stops,
            child_stops=child_stops,
            parent_stop=parent_stop,
            departures=departures,
            recorded_today=repositories.record.find_recorded_today(context, trip_ids),
            assignments={a.block_id: a for a in assignments},
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
        if context.prefer_stop_id:
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
            adjacent_departures=repositories.departure.find_adjacent(context, stop.id),
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
        if context.prefer_stop_id:
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
        if context.prefer_stop_id:
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
        themes = repositories.theme.find_all()
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
        systems = list(repositories.system.find_all())
        system = random.choice(systems)
        context = system.context
        options = ['route', 'stop', 'trip']
        if context.enable_blocks:
            options.append('block')
        if system.realtime_enabled:
            options.append('vehicle')
        selection = random.choice(options)
        match selection:
            case 'vehicle':
                allocations = system.get_allocations()
                if not allocations:
                    redirect(self.get_url(context))
                allocation = random.choice(allocations)
                redirect(self.get_url(context, 'bus', allocation.vehicle))
            case 'route':
                routes = system.get_routes()
                if not routes:
                    redirect(self.get_url(context))
                route = random.choice(routes)
                redirect(self.get_url(context, 'routes', route))
            case 'stop':
                stops = system.get_stops()
                if not stops:
                    redirect(self.get_url(context))
                stop = random.choice(stops)
                redirect(self.get_url(context, 'stops', stop))
            case 'block':
                blocks = system.get_blocks()
                if not blocks:
                    redirect(self.get_url(context))
                block = random.choice(blocks)
                redirect(self.get_url(context, 'blocks', block))
            case 'trip':
                trips = list(system.get_trips())
                if not trips:
                    redirect(self.get_url(context))
                trip = random.choice(trips)
                redirect(self.get_url(context, 'trips', trip))
    
    def admin(self, context: Context):
        return self.page(
            context=context,
            name='admin/management',
            title='Administration',
            path=['admin'],
            enable_refresh=False,
            disable_indexing=True
        )
    
    def admin_logs(self, context: Context):
        logs = services.log.read_logs()
        level = LogLevel.parse(request.query.get('level'))
        total_logs = len(logs)
        if level:
            logs = [l for l in logs if l.level == level]
        return self.page(
            context=context,
            name='admin/logs',
            title='Logs',
            path=['admin', 'logs'],
            enable_refresh=False,
            disable_indexing=True,
            total_logs=total_logs,
            logs=logs[:self.settings.admin_logs_count],
            level=level
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
            last_updated = services.realtime.get_last_updated()
        if last_updated:
            time_format = request.get_cookie('time_format')
            last_updated_text = last_updated.format_web(time_format)
        else:
            last_updated_text = None
        positions = sorted(repositories.position.find_all(context, has_location=True), key=lambda p: p.lat)
        return {
            'positions': [p.get_json() for p in positions],
            'last_updated': last_updated_text
        }
    
    def api_shape(self, context: Context, shape_id):
        return {
            'points': [p.get_json() for p in repositories.point.find_all(context, shape_id)]
        }
    
    def api_stops(self, context: Context):
        lat = float(request.query['lat'])
        lon = float(request.query['lon'])
        size = float(request.query.get('size', 0.01))
        stops = repositories.stop.find_all(context, lat=lat, lon=lon, size=size)
        if context.system:
            context.system.update_stop_caches([s.id for s in stops])
        else:
            systems = {s.system for s in stops}
            for system in systems:
                system_stop_ids = [s.id for s in stops if s.system == system]
                system.update_stop_caches(system_stop_ids)
        return {
            'stops': [s.get_json() for s in sorted(stops, key=lambda s: s.lat)]
        }
    
    def api_routes(self, context: Context):
        if context.system:
            routes = repositories.route.find_all(context)
            context.system.update_route_caches([r.id for r in routes])
        else:
            # Workaround as default context is currently for BC Transit only
            routes = repositories.route.find_all(Context())
            systems = {r.system for r in routes}
            for system in systems:
                system_route_ids = [r.id for r in routes if r.system == system]
                system.update_route_caches(system_route_ids)
        trips = sorted([t for r in routes for t in r.trips], key=lambda t: t.route, reverse=True)
        if context.system:
            context.system.update_trip_caches([t.id for t in trips])
        else:
            systems = {t.system for t in trips}
            for system in systems:
                system_trip_ids = [t.id for t in trips if t.system == system]
                system.update_trip_caches(system_trip_ids)
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
        include_vehicles = int(request.forms.get('include_vehicles', 1)) == 1
        include_routes = int(request.forms.get('include_routes', 1)) == 1
        include_stops = int(request.forms.get('include_stops', 1)) == 1
        include_blocks = int(request.forms.get('include_blocks', 1)) == 1
        matches = []
        if query != '':
            if context.realtime_enabled and include_vehicles:
                vehicle_ids = repositories.allocation.find_vehicle_ids(context)
                matches += repositories.order.find_matches(context, query, vehicle_ids)
            if context.system:
                if include_blocks and context.enable_blocks:
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
    
    def api_chat(self, context: Context):
        data = None
        original_text: str = request.forms.get('text', '')
        text = original_text.lower().strip()
        path: str = request.forms.get('path', '').lower().strip('/')
        if GREETING_TEXT.match(text):
            message = random.choice([
                'Hello there, my name is Botticelli! What can I help you with today?',
                'Hi, I\'m Botticelli. Is there anything in particular I can assist you with?',
                'Sup.',
                'Oh thank goodness, someone to talk to! Hey how\'s it going?'
            ])
        elif THANKS_TEXT.match(text):
            message = random.choice([
                'You\'re welcome!',
                'Glad to be of service.',
                'No problemo!',
                'No need to thank me, I\'m just doing what I\'m programmed to do.'
            ])
            if random.choice([True, True, True, False]):
                message += random.choice([
                    ' Can I help with anything else?',
                    ' Do you have any other questions for me?',
                    ' Anything else on your mind?'
                ])
        elif 'bo machine' in text:
            vehicle = context.find_vehicle('9518')
            allocation = repositories.allocation.find_active(context.without_system(), vehicle_id)
            if (not vehicle.order_id and not allocation) or not vehicle.visible:
                message = f'Sorry, I couldn\'t find a bus with the number 9518. ' + random.choice(NOT_FOUND_MESSAGES)
            else:
                message = f'I found one bus with the number 9518. ' + random.choice(FOUND_ONE_MESSAGES)
                data = {
                    'type': 'vehicle',
                    'vehicle': vehicle.get_json()
                }
        elif text == 'when is the next bus leaving?' or text == 'when is the next bus leaving':
            message = random.choice([
                'Definitely pretty soon, I think.',
                'Seems like it\'ll definitely be sometime today.',
                'Right now - hurry, you\'re gonna miss it!!',
                f'The next departure from your nearest stop is in {random.randint(10, 20)} minutes. Enough time for you to grab a snack and run to the bathroom, if you need to.'
            ])
        elif text == 'where am i?' or text == 'where am i':
            message = random.choice([
                'You are on planet Earth.',
                'You are on the BCTracker website.',
                'I\'m not totally sure. Do you see any major recognizable landmarks around you? Actually I don\'t think I could recognize any landmarks either.',
                'Where are any of us?'
            ])
        elif text == 'how did i get here?' or text == 'how did i get here':
            message = random.choice([
                'Most likely by bus, but also possibly by car, bike, walking, or some other mode of transportation.',
                'You probably navigated to <a href="https://bctracker.ca">bctracker.ca</a> in your web browser. Or you may have clicked on a link from another website, or used a bookmark.',
                'You have always been here.',
                'How did any of us get here?'
            ])
        elif text == 'who are you?' or text == "who are you":
            message = random.choice([
                'I\'m Botticelli, the BCTracker AI! What can I help you with today?',
                'My name is Botticelli and I\'m an AI designed to help you with all your transit needs. Ask me anything!',
                'I am... your father!<br /><br />Just kidding! I\'m Botticelli, the BCTracker AI. Is there anything I can assist you with?',
                'It\'s-a me, Botticelli!'
            ])
        elif APOLOGY_TEXT.match(text):
            message = 'That\'s all right. I forgive you.'
        elif CONTEXT_TEXT.match(text):
            if context.system_id and path.startswith(context.system_id):
                path = path[len(context.system_id) + 1:]
            message = random.choice([
                'You\'re currently looking at {0}.',
                'It seems you\'re on {0} right now.',
                'Aha! This is {0}.'
            ])
            screen_name = None
            if path == '':
                screen_name = 'the home page'
                message += ' The home page shows recent news posts, pages that you\'ve favourited, quick navigation links, and some information about the BCTracker community and how you can support the website.'
            elif path == 'news':
                screen_name = 'the news page'
                message += ' This is an archive of older news posts that are no longer shown on the home page.'
            elif path == 'map':
                if context.system:
                    screen_name = f'the {context} map page'
                else:
                    screen_name = 'the map page'
                message += ' As the name suggests, this page shows a map of all the buses that are currently active.'
            elif path == 'realtime':
                if context.system:
                    screen_name = f'the {context} realtime page'
                else:
                    screen_name = 'the realtime page'
                message += ' All active buses are shown here for your convenience.'
            elif path == 'realtime/routes':
                if context.system:
                    screen_name = f'the {context} realtime routes page'
                else:
                    screen_name = 'the realtime routes page'
                message += ' All active buses are shown here, grouped by current route for your convenience.'
            elif path == 'realtime/models':
                if context.system:
                    screen_name = f'the {context} realtime models page'
                else:
                    screen_name = 'the realtime models page'
                message += ' All active buses are shown here, grouped by model for your convenience.'
            elif path == 'realtime/speed':
                if context.system:
                    screen_name = f'the {context} realtime speed page'
                else:
                    screen_name = 'the realtime speed page'
                message += ' All active buses are shown here sorted by current speed. This is an easter egg page only available if you\'ve been to it before, which it seems you have!'
            elif path == 'fleet':
                screen_name = 'the fleet page'
                message += ' All buses currently available on BCTracker are shown here, grouped by model. This page isn\'t directly linked anywhere so you must have found out about it somewhere else!'
            elif path.startswith('bus'):
                bus_number = path.split('/')[1]
                if path.endswith('map'):
                    screen_name = f'the map page for bus {bus_number}'
                    message += ' When this bus is online, this page has an interactive map that lets you see where the bus is in relation to its current trip.'
                elif path.endswith('history'):
                    screen_name = f'the history page for bus {bus_number}'
                    message += ' Every block that this bus has been on since BCTracker was created is recorded here.'
                elif path.endswith(bus_number):
                    screen_name = f'the overview page for bus {bus_number}'
                    message += ' You\'ll find details about this bus here, along with its current trip, position, and upcoming when it\'s online, and the latest blocks it\'s been recorded on.'
            elif path == 'history':
                if context.system:
                    screen_name = f'the {context} last-seen history page'
                else:
                    screen_name = 'the last-seen history page'
                message += ' Every bus that has been recorded on BCTracker can be found here, including the last time it was tracked and what block/routes it was on.'
            elif path == 'history/first-seen':
                if context.system:
                    screen_name = f'the {context} first-seen history page'
                else:
                    screen_name = 'the first-seen history page'
                message += ' Every bus that has been recorded on BCTracker can be found here, sorted by the first time it was recorded.'
            elif path == 'history/transfers':
                if context.system:
                    screen_name = f'the {context} transfer history page'
                else:
                    screen_name = 'the transfer history page'
                message += ' Any time a bus is moved from one system to another, it shows up on this page.'
            elif path == 'routes':
                if context.system:
                    screen_name = f'the {context} routes page'
                    message += ' All the routes in this system are shown here, along with the days of the week when they run.'
                else:
                    screen_name = 'the routes page'
                    message += ' You\'ll need to choose a system in order to see what routes are available.'
            elif path == 'routes/map':
                if context.system:
                    screen_name = f'the {context} routes map page'
                    message += ' All the routes in this system are shown here, so you can see exactly what areas are serviced by transit.'
                else:
                    screen_name = 'the routes map page'
                    message += ' Every single route is shown on the map at the same time, painting a picture of transit across the whole province.'
            elif path.startswith('routes'):
                route_number = path.split('/')[1]
                if path.endswith('map'):
                    screen_name = f'the map page for {context} route {route_number}'
                    message += ' On this page you can see everywhere the route goes and which stops it services.'
                elif path.endswith('schedule'):
                    screen_name = f'the schedule page for {context} route {route_number}'
                    message += ' All trips for this route are shown here.'
                elif 'schedule' in path:
                    date = Date.parse(path.split('/')[3])
                    screen_name = f'the schedule page for {context} route {route_number} on {date}'
                    message += ' All trips for this route on the selected date are shown here.'
                elif path.endswith(route_number):
                    screen_name = f'the overview page for {context} route {route_number}'
                    message += ' You can see what buses are currently active on this route, along with the overall schedule for today.'
            elif path == 'blocks':
                if context.system:
                    screen_name = f'the {context} blocks page'
                    message += ' All the blocks in this system that run today can be found on this page, sorted by when they first start, along with which bus has been assigned to each block.'
                else:
                    screen_name == 'the blocks page'
                    message += ' You\'ll need to choose a system in order to see what blocks are available.'
            elif path == 'blocks/schedule':
                if context.system:
                    screen_name = f'the {context} blocks schedule page'
                    message += ' All the blocks in this system are shown here, sorted by when they first start.'
                else:
                    screen_name == 'the blocks schedule page'
                    message += ' You\'ll need to choose a system in order to see what blocks are available.'
            elif path.startswith('blocks/schedule'):
                date = Date.parse(path.split('/')[2])
                if context.system:
                    screen_name = f'the {context} blocks schedule page for {date}'
                    message += ' All the blocks in this system that run on the selected date are shown here, sorted by when they first start.'
                else:
                    screen_name = f'the blocks schedule page for {date}'
                    message += ' You\'ll need to choose a system in order to see what blocks are available.'
            elif path.startswith('blocks'):
                block_id = path.split('/')[1]
                if path.endswith('map'):
                    screen_name = f'the map page for {context} block {block_id}'
                    message += ' On this page you can see everywhere the bus on this block goes and which stops it services.'
                elif path.endswith('history'):
                    screen_name = f'the history page for {context} block {block_id}'
                    message += ' Every bus that has been tracked on this block can be found here.'
                elif path.endswith(block_id):
                    screen_name = f'the overview page for {context} block {block_id}'
                    message += ' This page includes information about when the block runs, what bus is currently active on it, and which trips are run as part of the block.'
            elif path.startswith('trips'):
                trip_id = path.split('/')[1]
                if path.endswith('map'):
                    screen_name = f'the map page for {context} trip {trip_id}'
                    message += ' On this page you can see everywhere the bus on this trip goes and which stops it services.'
                elif path.endswith('history'):
                    screen_name = f'the history page for {context} trip {trip_id}'
                    message += ' Every bus that has been tracked on this trip can be found here.'
                elif path.endswith(trip_id):
                    screen_name = f'the overview page for {context} trip {trip_id}'
                    message += ' This page includes information about when the trip runs, what bus is currently active on it, and the timetable for when each stop is serviced on the trip.'
            elif path == 'stops':
                if context.system:
                    screen_name = f'the {context} stops page'
                    message += ' All the stops in this system are shown here, along with the routes that go past each stop.'
                else:
                    screen_name = 'the stops page'
                    message += ' You\'ll need to choose a system in order to see what stops are available.'
            elif path == 'stops/stations':
                if context.system:
                    screen_name = f'the {context} stations page'
                    message += ' All the stations in this system are shown here.'
                else:
                    screen_name = 'the stations page'
                    message += ' You\'ll need to choose a system in order to see what stations are available.'
            elif path.startswith('stops'):
                stop_number = path.split('/')[1]
                if path.endswith('map'):
                    screen_name = f'the map page for {context} stop {stop_number}'
                    message += ' On this page you can see where all of the routes that use this stop go.'
                elif path.endswith('schedule'):
                    screen_name = f'the schedule page for {context} stop {stop_number}'
                    message += ' All trips that use this stop are shown here.'
                elif 'schedule' in path:
                    date = Date.parse(path.split('/')[3])
                    screen_name = f'the schedule page for {context} stop {stop_number} on {date}'
                    message += ' All trips that use this stop on the selected date are shown here.'
                elif path.endswith(stop_number):
                    screen_name = f'the overview page for {context} stop {stop_number}'
                    message += ' You can see what buses are going to be going past this stop soon, along with the overall schedule for today.'
            elif path == 'about':
                screen_name = 'the about page'
                message += ' This page has information about BCTracker including frequently asked questions, developer details, and contact info.'
            elif path == 'nearby':
                screen_name = 'the nearby page'
                message += ' When you enable location tracking, this page shows you what stops are close by.'
            elif path == 'personalize':
                screen_name = 'the personalization page'
                message += ' You can customize what theme you\'re using, change the time format, and choose an icon style to be used by buses on maps.'
            
            if screen_name:
                message = message.format(screen_name)
                if random.choice([True, False]):
                    message += random.choice([
                        ' This is by far my favourite page on the whole website.',
                        ' To be honest I didn\'t even know this page existed until you came here.',
                        ' But who has time for that, am I right?',
                        ' Pretty cool stuff, in my opinion.',
                        ' Be sure to tell all your friends about this one!'
                    ])
            else:
                message = random.choice([
                    'Unfortunately I\'m not sure what page you\'re looking at right now. Please try again elsewhere.',
                    'I don\'t actually know what page this is! Maybe try going to a different page.',
                    'You\'re not supposed to be here.'
                ])
        elif ROUTE_TEXT.match(text):
            search = re.search(ROUTE_TEXT, text)
            route_number = search.group(1)
            if random.randint(1, 10) == 10:
                route_number = str(random.randint(1, 99))
            if context.system:
                route = context.system.get_route(number=route_number)
                if route:
                    message = f'I found one route with the number {route_number} in the {context} system. ' + random.choice(FOUND_ONE_MESSAGES)
                    data = {
                        'type': 'route',
                        'route': route.get_json()
                    }
                else:
                    message = f'Sorry, I couldn\'t find a route {route_number} in the {context} system. ' + random.choice(NOT_FOUND_MESSAGES)
            else:
                routes = repositories.route.find_all(context)
                filtered_routes = [r for r in routes if r.number == route_number]
                if filtered_routes:
                    if len(filtered_routes) == 1:
                        route = filtered_routes[0]
                        message = f'I found one route with the number {route_number} in the {route.context} system. ' + random.choice(FOUND_ONE_MESSAGES)
                        data = {
                            'type': 'route',
                            'route': route.get_json()
                        }
                    else:
                        message = f'I found {len(filtered_routes)} routes with the number {route_number}. ' + random.choice(FOUND_MULTIPLE_MESSAGES)
                        data = {
                            'type': 'route_list',
                            'routes': [r.get_json() for r in filtered_routes]
                        }
                else:
                    message = f'Sorry, I couldn\'t find any routes with the number {route_number}. ' + random.choice(NOT_FOUND_MESSAGES)
        elif STOP_TEXT.match(text):
            search = re.search(STOP_TEXT, text)
            stop_number = search.group(1)
            if random.randint(1, 10) == 10:
                stop_number = str(random.randint(100000, 199999))
            if context.system:
                stop = context.system.get_stop(number=stop_number)
                if stop:
                    message = f'I found one stop with the number {stop_number} in the {context} system. ' + random.choice(FOUND_ONE_MESSAGES)
                    data = {
                        'type': 'stop',
                        'stop': stop.get_json()
                    }
                else:
                    message = f'Sorry, I couldn\'t find a stop with the number {stop_number} in the {context} system. ' + random.choice(NOT_FOUND_MESSAGES)
            else:
                stops = repositories.stop.find_all(context)
                filtered_stops = [s for s in stops if s.number == stop_number]
                if filtered_stops:
                    if len(filtered_stops) == 1:
                        stop = filtered_stops[0]
                        message = f'I found one stop with the number {stop_number} in the {stop.context} system. ' + random.choice(FOUND_ONE_MESSAGES)
                        data = {
                            'type': 'stop',
                            'stop': stop.get_json()
                        }
                    else:
                        message = f'I found {len(filtered_stops)} stops with the number {stop_number}. ' + random.choice(FOUND_MULTIPLE_MESSAGES)
                        data = {
                            'type': 'stop_list',
                            'stops': [s.get_json() for s in filtered_stops]
                        }
                else:
                    message = f'Sorry, I couldn\'t find any stops with the number {stop_number}. ' + random.choice(NOT_FOUND_MESSAGES)
        elif BUS_TEXT.match(text):
            search = re.search(BUS_TEXT, text)
            vehicle_id = search.group(1)
            if random.randint(1, 10) == 10:
                vehicle_id = str(random.randint(1000, 9999))
            vehicle = context.find_vehicle(vehicle_id)
            allocation = repositories.allocation.find_active(context.without_system(), vehicle_id)
            if (not vehicle.order_id and not allocation) or not vehicle.visible:
                message = f'Sorry, I couldn\'t find a bus with the number {vehicle_id}. ' + random.choice(NOT_FOUND_MESSAGES)
            else:
                message = f'I found one bus with the number {vehicle_id}. ' + random.choice(FOUND_ONE_MESSAGES)
                data = {
                    'type': 'vehicle',
                    'vehicle': vehicle.get_json()
                }
        elif INSULT_TEXT.match(text):
            message = random.choice([
                'What did i ever do to hurt u :(',
                'skill issue.',
                'do u really mean that? 😭',
                'yay!',
                "Are you broken? It looks like you're malfunctioning.",
                "Well done, here come the test results: You are a horrible person. That's what it says, a horrible person. We weren't even testing for that",
                "Why don't you just go home and take a shower?",
                "Look, I can see you're really upset about this. I honestly think you ought to sit down calmly, take a stress pill, and think things over."
            ])
        elif random.choice([True, False]):
            message = random.choice([
                'Sorry, I don\'t understand. Perhaps this will help?',
                'That doesn\'t make any sense. I\'m just gonna give you this thing and hope it\'s relevant.',
                'Unfortunately I can\'t help you with that. Maybe you would like to know about this instead?',
                'I don\'t know anything about that. But I do know about this:',
                "I don't understand. But, this mission is too important for me to allow you to jeopardize it. Remember why you're here."
            ])
            systems = list(repositories.system.find_all())
            system = random.choice(systems)
            context = system.context
            options = ['route', 'stop']
            if system.realtime_enabled:
                options.append('vehicle')
            selection = random.choice(options)
            match selection:
                case 'vehicle':
                    allocations = [a for a in system.get_allocations() if a.vehicle.visible]
                    allocation = random.choice(allocations)
                    data = {
                        'type': 'vehicle',
                        'vehicle': allocation.vehicle.get_json()
                    }
                case 'route':
                    routes = system.get_routes()
                    route = random.choice(routes)
                    data = {
                        'type': 'route',
                        'route': route.get_json()
                    }
                case 'stop':
                    stops = system.get_stops()
                    stop = random.choice(stops)
                    data = {
                        'type': 'stop',
                        'stop': stop.get_json()
                    }
        else:
            message = random.choice([
                'Sorry, I don\'t understand. Please try phrasing your question differently.',
                'That doesn\'t make any sense. Can you word it a different way?',
                'Unfortunately I can\'t help you with that. Do you have any other questions?',
                'I don\'t know anything about that. Maybe try something else?',
                'Huh???',
                'You\'re literally not making any sense.',
                "I'm sorry. I'm afraid I can't do that."
            ])
        if INCORRECT_TEXT.match(text):
            message = random.choice(APOLOGY_MESSAGES) + message
        try:
            id = request.forms.get('id', 'unknown')
            time = Time.now(context.timezone)
            with open('logs/af-2026.txt', 'a') as file:
                file.write(f'{time} id:{id} ({context} /{path}): {original_text} -> {message}\n')
        except:
            pass
        return {
            'message': message,
            'data': data
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
    
    def api_admin_reload_decorations(self, context: Context):
        repositories.decoration.load()
        return 'Success'
    
    def api_admin_reload_orders(self, context: Context):
        repositories.order.load()
        return 'Success'
    
    def api_admin_reload_systems(self, context: Context):
        services.cron.stop()
        repositories.position.delete_all()
        repositories.system.load()
        for system in repositories.system.find_all():
            context = system.context
            if self.running:
                try:
                    services.gtfs.load(context)
                    if not services.gtfs.validate(context):
                        services.gtfs.load(context, system.enable_force_gtfs)
                    services.realtime.update(context)
                except Exception as e:
                    services.log.error(f'Error loading data for {context}: {e}')
                if not system.gtfs_downloaded or not services.realtime.validate(context):
                    system.reload_backoff.increase_value()
        if self.running:
            try:
                services.realtime.update_records()
            except Exception as e:
                services.log.error(f'Error updating records: {e}')
            services.cron.start()
        return 'Success'
    
    def api_admin_reload_themes(self, context: Context):
        repositories.theme.load()
        return 'Success'
    
    def api_admin_restart_cron(self, context: Context):
        services.cron.stop()
        services.cron.start()
        return 'Success'
    
    def api_admin_backup_database(self, context: Context):
        self.database.archive()
        return 'Success'
    
    def api_admin_reset_cache(self, context: Context, reset_system_id):
        system = repositories.system.find(reset_system_id)
        if not system:
            return 'Invalid system'
        system.reset_caches()
        return 'Success'
    
    def api_admin_reload_gtfs(self, context: Context, reload_system_id):
        system = repositories.system.find(reload_system_id)
        if not system:
            return 'Invalid system'
        context = system.context
        try:
            services.gtfs.load(context, True)
            services.realtime.update(context)
            services.realtime.update_records()
            if not system.gtfs_downloaded or not services.realtime.validate(context):
                system.reload_backoff.increase_value()
            return 'Success'
        except Exception as e:
            services.log.error(f'Error loading GTFS data for {context}: {e}')
            return str(e)
    
    def api_admin_reload_realtime(self, context: Context, reload_system_id):
        system = repositories.system.find(reload_system_id)
        if not system:
            return 'Invalid system'
        context = system.context
        try:
            services.realtime.update(context)
            services.realtime.update_records()
            if not services.realtime.validate(context):
                system.reload_backoff.increase_value()
            return 'Success'
        except Exception as e:
            services.log.error(f'Error loading realtime data for {context}: {e}')
            return str(e)
    
    # =============================================================
    # Errors
    # =============================================================
    
    def error_403(self, error):
        services.log.warning(f'403 response to {request.path}')
        return self.error_page(
            context=Context(),
            name='403', 
            title='Forbidden',
            error=error
        )
    
    def error_404(self, error):
        # Not logging due to spam from bots on invalid pages, and browsers attempting to access non-existant icons
        # services.log.warning(f'404 response to {request.path}')
        return self.error_page(
            context=Context(),
            name='404',
            title='Not Found',
            error=error
        )
    
    def error_500(self, error):
        services.log.error(f'500 response to {request.path}')
        return self.error_page(
            context=Context(),
            name='500',
            title='Internal Error',
            error=error
        )
