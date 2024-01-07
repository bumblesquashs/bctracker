
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, HTTPError, static_file, template, request, response, debug, redirect
import cherrypy as cp

import helpers.adornment
import helpers.model
import helpers.order
import helpers.overview
import helpers.point
import helpers.position
import helpers.record
import helpers.region
import helpers.stop
import helpers.system
import helpers.theme
import helpers.transfer

from models.bus import Bus
from models.date import Date
from models.event import Event

import cron
import database
import gtfs
import realtime

# Increase the version to force CSS reload
VERSION = 23

app = Bottle()
running = False

cron_id = 'bctracker-muncher'
mapbox_api_key = ''
no_system_domain = 'https://bctracker.ca/{0}'
system_domain = 'https://{0}.bctracker.ca/{1}'
system_domain_path = 'https://bctracker.ca/{0}/{1}'
cookie_domain = None
admin_key = None

def start(args):
    '''Loads all required data and launches the server'''
    global running, cron_id, mapbox_api_key, no_system_domain, system_domain, system_domain_path, cookie_domain, admin_key
    
    running = True
    
    database.connect()
    
    if args.debug:
        print('Starting bottle in DEBUG mode')
        debug(True)
    if args.reload:
        print('Forcing GTFS redownload')
    if args.updatedb:
        print('Forcing database refresh')
    
    helpers.adornment.load()
    helpers.model.load()
    helpers.order.load()
    helpers.region.load()
    helpers.system.load()
    helpers.theme.load()
    
    helpers.position.delete_all()
    
    cp.config.update('server.conf')
    cron_id = cp.config.get('cron_id', 'bctracker-muncher')
    mapbox_api_key = cp.config['mapbox_api_key']
    no_system_domain = cp.config['no_system_domain']
    system_domain = cp.config['system_domain']
    system_domain_path = cp.config['system_domain_path']
    cookie_domain = cp.config.get('cookie_domain')
    admin_key = cp.config.get('admin_key')
    
    handler = TimedRotatingFileHandler(filename='logs/access_log.log', when='d', interval=7)
    log = WSGILogger(app, [handler], ApacheFormatter())
    
    cp.tree.graft(log, '/')
    cp.server.start()
    
    for system in helpers.system.find_all():
        if running:
            gtfs.load(system, args.reload, args.updatedb)
            if not gtfs.validate(system):
                gtfs.load(system, True)
            gtfs.update_cache_in_background(system)
            realtime.update(system)
            if not realtime.validate(system):
                system.validation_errors += 1
    if running:
        realtime.update_records()
        
        cron.setup()
        cron.start(cron_id)

def stop():
    '''Terminates the server'''
    global running
    running = False
    cron.stop(cron_id)
    database.disconnect()
    if cp.server.running:
        cp.server.stop()

def get_url(system, path='', **kwargs):
    '''Returns a URL formatted based on the given system and path'''
    system_id = getattr(system, 'id', system)
    if system_id is None:
        url = no_system_domain.format(path).rstrip('/')
    else:
        url = system_domain.format(system_id, path).rstrip('/')
    query_args = {k:v for k, v in kwargs.items() if v is not None}
    if len(query_args) > 0:
        query = '&'.join([f'{k}={v}' for k, v in query_args.items()])
        url += f'?{query}'
    return url

def page(name, system, title, path='', path_args=None, enable_refresh=True, include_maps=False, full_map=False, **kwargs):
    '''Returns an HTML page with the given name and details'''
    theme_id = request.query.get('theme') or request.get_cookie('theme')
    time_format = request.query.get('time_format') or request.get_cookie('time_format')
    bus_marker_style = request.query.get('bus_marker_style') or request.get_cookie('bus_marker_style')
    hide_systems = request.get_cookie('hide_systems') == 'yes'
    if system is None:
        last_updated = realtime.get_last_updated(time_format)
    else:
        last_updated = system.get_last_updated(time_format)
    return template(f'pages/{name}',
        version=VERSION,
        title=title,
        path=path,
        path_args=path_args or {},
        enable_refresh=enable_refresh,
        include_maps=include_maps,
        full_map=full_map,
        regions=helpers.region.find_all(),
        systems=[s for s in helpers.system.find_all() if s.enabled and s.visible],
        admin_systems=helpers.system.find_all(),
        system=system,
        get_url=get_url,
        no_system_domain=no_system_domain,
        system_domain=system_domain,
        system_domain_path=system_domain_path,
        cookie_domain=cookie_domain,
        mapbox_api_key=mapbox_api_key,
        last_updated=last_updated,
        theme=helpers.theme.find(theme_id),
        time_format=time_format,
        bus_marker_style=bus_marker_style,
        hide_systems=hide_systems,
        show_speed=request.get_cookie('speed') == '1994',
        show_survey_banner=request.get_cookie('survey_banner', 'show') == 'show',
        **kwargs
    )

def error_page(name, system, title='Error', path='', **kwargs):
    '''Returns an error page with the given name and details'''
    return page(f'errors/{name}', system,
        title=title,
        path=path,
        enable_refresh=False,
        **kwargs
    )

def frame(name, system, **kwargs):
    return template(f'frames/{name}',
        system=system,
        get_url=get_url,
        time_format=request.get_cookie('time_format'),
        show_speed=request.get_cookie('speed') == '1994',
        **kwargs
    )

def set_cookie(key, value):
    '''Creates a cookie using the given key and value'''
    max_age = 60*60*24*365*10
    if cookie_domain is None:
        response.set_cookie(key, value, max_age=max_age, path='/')
    else:
        response.set_cookie(key, value, max_age=max_age, domain=cookie_domain, path='/')

def query_cookie(key, default_value):
    '''Creates a cookie if a query value exists, otherwise uses the existing cookie value'''
    value = request.query.get(key)
    if value is not None:
        set_cookie(key, value)
        return value
    return request.get_cookie(key, default_value)

def endpoint(base_path, method='GET', append_slash=True, system_key='system_id'):
    def endpoint_wrapper(func):
        if base_path == '/':
            paths = [
                base_path,
                f'/<{system_key}>'
            ]
            if append_slash:
                paths.append(f'/<{system_key}>/')
        else:
            paths = [
                base_path,
                f'/<{system_key}>{base_path}'
            ]
            if append_slash:
                paths.append(f'{base_path}/')
                paths.append(f'/<{system_key}>{base_path}/')
        @app.route(paths, method)
        def func_wrapper(*args, **kwargs):
            if system_key in kwargs:
                system_id = kwargs[system_key]
                system = helpers.system.find(system_id)
                if system is None:
                    raise HTTPError(404)
                del kwargs[system_key]
            else:
                system = None
            return func(system=system, *args, **kwargs)
        return func_wrapper
    return endpoint_wrapper

# =============================================================
# Static Files
# =============================================================

@endpoint('/style/<name:path>', append_slash=False)
def style(system, name):
    return static_file(name, root='./style')

@endpoint('/img/<name:path>', append_slash=False)
def img(system, name):
    return static_file(name, root='./img')

@endpoint('/robots.txt', append_slash=False)
def robots_text(system):
    return static_file('robots.txt', root='.')

# =============================================================
# Pages
# =============================================================

@endpoint('/')
def home_page(system):
    return page('home', system,
        title='Home',
        enable_refresh=False
    )

@endpoint('/news')
def news_page(system):
    return page('news', system,
        title='News Archive',
        path='news',
        enable_refresh=False
    )

@endpoint('/map')
def map_page(system):
    positions = helpers.position.find_all(system, has_location=True)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    visible_positions = positions if show_nis else [p for p in positions if p.trip is not None]
    return page('map', system,
        title='Map',
        path='map',
        include_maps=len(visible_positions) > 0,
        full_map=len(visible_positions) > 0,
        positions=sorted(positions, key=lambda p: p.lat, reverse=True),
        show_nis=show_nis,
        visible_positions=visible_positions
    )

@endpoint('/realtime')
def realtime_all_page(system):
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip is not None]
    return page('realtime/all', system,
        title='Realtime',
        path='realtime',
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/realtime/routes')
def realtime_routes_page(system):
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip is not None]
    return page('realtime/routes', system,
        title='Realtime',
        path='realtime/routes',
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/realtime/models')
def realtime_models_page(system):
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip is not None]
    return page('realtime/models', system,
        title='Realtime',
        path='realtime/models',
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/realtime/speed')
def realtime_speed_page(system):
    set_cookie('speed', '1994')
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip is not None]
    return page('realtime/speed', system,
        title='Realtime',
        path='realtime/speed',
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/fleet')
def fleet_page(system):
    orders = helpers.order.find_all()
    overviews = helpers.overview.find_all()
    return page('fleet', system,
        title='Fleet',
        path='fleet',
        orders=[o for o in sorted(orders) if o.visible],
        overviews={o.bus.number: o for o in overviews}
    )

@endpoint('/bus/<bus_number:int>')
def bus_overview_page(system, bus_number):
    bus = Bus(bus_number)
    overview = helpers.overview.find(bus)
    if (bus.order is None and overview is None) or not bus.visible:
        return error_page('invalid_bus', system,
            bus_number=bus_number
        )
    position = helpers.position.find(bus)
    records = helpers.record.find_all(bus=bus, limit=20)
    return page('bus/overview', system,
        title=f'Bus {bus}',
        include_maps=position is not None,
        bus=bus,
        position=position,
        records=records,
        overview=overview
    )

@endpoint('/bus/<bus_number:int>/map')
def bus_map_page(system, bus_number):
    bus = Bus(bus_number)
    overview = helpers.overview.find(bus)
    if (bus.order is None and overview is None) or not bus.visible:
        return error_page('invalid_bus', system,
            bus_number=bus_number
        )
    position = helpers.position.find(bus)
    return page('bus/map', system,
        title=f'Bus {bus}',
        include_maps=position is not None,
        full_map=position is not None,
        bus=bus,
        position=position
    )

@endpoint('/bus/<bus_number:int>/history')
def bus_history_page(system, bus_number):
    bus = Bus(bus_number)
    overview = helpers.overview.find(bus)
    if (bus.order is None and overview is None) or not bus.visible:
        return error_page('invalid_bus', system,
            bus_number=bus_number
        )
    records = helpers.record.find_all(bus=bus)
    transfers = helpers.transfer.find_all(bus=bus)
    events = []
    if overview is not None:
        events.append(Event(overview.first_seen_date, 'First Seen'))
        if overview.first_record is not None:
            events.append(Event(overview.first_record.date, 'First Tracked'))
        events.append(Event(overview.last_seen_date, 'Last Seen'))
        if overview.last_record is not None:
            events.append(Event(overview.last_record.date, 'Last Tracked'))
        for transfer in transfers:
            events.append(Event(transfer.date, 'Transferred',  f'{transfer.old_system} to {transfer.new_system}'))
    return page('bus/history', system,
        title=f'Bus {bus}',
        bus=bus,
        records=records,
        overview=overview,
        events=events
    )

@endpoint('/history')
def history_last_seen_page(system):
    overviews = [o for o in helpers.overview.find_all(system) if o.last_record is not None and o.bus.visible]
    return page('history/last_seen', system,
        title='Vehicle History',
        path='history',
        overviews=sorted(overviews, key=lambda o: o.bus)
    )

@endpoint('/history/first-seen')
def history_first_seen_page(system):
    overviews = [o for o in helpers.overview.find_all(system) if o.first_record is not None and o.bus.visible]
    return page('history/first_seen', system,
        title='Vehicle History',
        path='history/first-seen',
        overviews=sorted(overviews, key=lambda o: (o.first_record.date, o.first_record.first_seen, o.bus), reverse=True)
    )

@endpoint('/history/transfers')
def history_transfers_page(system):
    transfers = helpers.transfer.find_all(system)
    return page('history/transfers', system,
        title='Vehicle History',
        path='history/transfers',
        transfers=[t for t in transfers if t.bus.visible]
    )

@endpoint('/routes')
def routes_list_page(system):
    return page('routes/list', system,
        title='Routes',
        path='routes',
        enable_refresh=False
    )

@endpoint('/routes/map')
def routes_map_page(system):
    if system is None:
        routes = []
    else:
        routes = system.get_routes()
    return page('routes/map', system,
        title='Routes',
        path='routes/map',
        enable_refresh=False,
        include_maps=len(routes) > 0,
        full_map=len(routes) > 0,
        routes=routes
    )

@endpoint('/routes/<route_number>')
def route_overview_page(system, route_number):
    if system is None:
        return error_page('system_required', system,
            path=f'routes/{route_number}'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('invalid_route', system,
            route_number=route_number
        )
    trips = sorted(route.get_trips(date=Date.today()))
    return page('route/overview', system,
        title=str(route),
        include_maps=len(route.trips) > 0,
        route=route,
        trips=trips,
        recorded_today=helpers.record.find_recorded_today(system, trips),
        scheduled_today=helpers.record.find_scheduled_today(system, trips),
        positions=helpers.position.find_all(system, route=route)
    )

@endpoint('/routes/<route_number>/map')
def route_map_page(system, route_number):
    if system is None:
        return error_page('system_required', system,
            path=f'routes/{route_number}/map'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('invalid_route', system,
            route_number=route_number
        )
    return page('route/map', system,
        title=str(route),
        include_maps=len(route.trips) > 0,
        full_map=len(route.trips) > 0,
        route=route,
        positions=helpers.position.find_all(system, route=route)
    )

@endpoint('/routes/<route_number>/schedule')
def route_schedule_page(system, route_number):
    if system is None:
        return error_page('system_required', system,
            path=f'routes/{route_number}/schedule'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('invalid_route', system,
            route_number=route_number
        )
    return page('route/schedule', system,
        title=str(route),
        enable_refresh=False,
        route=route
    )

@endpoint('/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>')
def route_schedule_date_page(system, route_number, date_string):
    if system is None:
        return error_page('system_required', system,
            path=f'routes/{route_number}/schedule'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('invalid_route', system,
            route_number=route_number
        )
    date = Date.parse_db(date_string, None)
    return page('route/date', system,
        title=str(route),
        enable_refresh=False,
        route=route,
        date=date
    )

@endpoint('/blocks')
def blocks_page(system):
    return page('blocks/list', system,
        title='Blocks',
        enable_refresh=False,
        path='blocks'
    )

@endpoint('/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>')
def blocks_schedule_date_page(system, date_string):
    date = Date.parse_db(date_string, None)
    return page('blocks/date', system,
        title='Blocks',
        enable_reload=False,
        path=f'blocks/schedule/{date_string}',
        date=date
    )

@endpoint('/blocks/<block_id>')
def block_overview_page(system, block_id):
    if system is None:
        return error_page('system_required', system,
            path=f'blocks/{block_id}'
        )
    block = system.get_block(block_id)
    if block is None:
        return error_page('invalid_block', system,
            block_id=block_id
        )
    return page('block/overview', system,
        title=f'Block {block.id}',
        include_maps=True,
        block=block,
        positions=helpers.position.find_all(system, block=block)
    )

@endpoint('/blocks/<block_id>/map')
def block_map_page(system, block_id):
    if system is None:
        return error_page('system_required', system,
            path=f'blocks/{block_id}/map'
        )
    block = system.get_block(block_id)
    if block is None:
        return error_page('invalid_block', system,
            block_id=block_id
        )
    return page('block/map', system,
        title=f'Block {block.id}',
        include_maps=True,
        full_map=True,
        block=block,
        positions=helpers.position.find_all(system, block=block)
    )

@endpoint('/blocks/<block_id>/history')
def block_history_page(system, block_id):
    if system is None:
        return error_page('system_required', system,
            path=f'blocks/{block_id}/history'
        )
    block = system.get_block(block_id)
    if block is None:
        return error_page('invalid_block', system,
            block_id=block_id
        )
    records = helpers.record.find_all(system, block=block)
    events = []
    if len(records) > 0:
        events.append(Event(records[0].date, 'Last Tracked'))
        events.append(Event(records[-1].date, 'First Tracked'))
    return page('block/history', system,
        title=f'Block {block.id}',
        block=block,
        records=records,
        events=events
    )

@endpoint('/trips/<trip_id>')
def trip_overview_page(system, trip_id):
    if system is None:
        return error_page('system_required', system,
            path=f'trips/{trip_id}'
        )
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('invalid_trip', system,
            trip_id=trip_id
        )
    return page('trip/overview', system,
        title=f'Trip {trip.id}',
        include_maps=True,
        trip=trip,
        positions=helpers.position.find_all(system, trip=trip)
    )

@endpoint('/trips/<trip_id>/map')
def trip_map_page(system, trip_id):
    if system is None:
        return error_page('system_required', system,
            path=f'trips/{trip_id}/map'
        )
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('invalid_trip', system,
            trip_id=trip_id
        )
    return page('trip/map', system,
        title=f'Trip {trip.id}',
        include_maps=True,
        full_map=True,
        trip=trip,
        positions=helpers.position.find_all(system, trip=trip)
    )

@endpoint('/trips/<trip_id>/history')
def trip_history_page(system, trip_id):
    if system is None:
        return error_page('system_required', system,
            path=f'trips/{trip_id}/history'
        )
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('invalid_trip', system,
            trip_id=trip_id
        )
    records = helpers.record.find_all(system, trip=trip)
    events = []
    if len(records) > 0:
        events.append(Event(records[0].date, 'Last Tracked'))
        events.append(Event(records[-1].date, 'First Tracked'))
    return page('trip/history', system,
        title=f'Trip {trip.id}',
        trip=trip,
        records=records,
        events=events
    )

@endpoint('/stops')
def stops_page(system):
    path = 'stops'
    search = request.query.get('search')
    if search is not None:
        path += f'?search={search}'
    return page('stops', system,
        title='Stops',
        enable_refresh=False,
        path=path,
        search=search
    )

@endpoint('/stops/<stop_number>')
def stop_overview_page(system, stop_number):
    if system is None:
        return error_page('system_required', system,
            path=f'stops/{stop_number}'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('invalid_stop', system,
            stop_number=stop_number
        )
    departures = stop.find_departures(date=Date.today())
    trips = [d.trip for d in departures]
    positions = helpers.position.find_all(system, trip=trips)
    return page('stop/overview', system,
        title=f'Stop {stop.number}',
        include_maps=True,
        stop=stop,
        departures=departures,
        recorded_today=helpers.record.find_recorded_today(system, trips),
        scheduled_today=helpers.record.find_scheduled_today(system, trips),
        positions={p.trip.id: p for p in positions}
    )

@endpoint('/stops/<stop_number>/map')
def stop_map_page(system, stop_number):
    if system is None:
        return error_page('system_required', system,
            path=f'stops/{stop_number}/map'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('invalid_stop', system,
            stop_number=stop_number
        )
    return page('stop/map', system,
        title=f'Stop {stop.number}',
        include_maps=True,
        full_map=True,
        stop=stop
    )

@endpoint('/stops/<stop_number>/schedule')
def stop_schedule_page(system, stop_number):
    if system is None:
        return error_page('system_required', system,
            path=f'stops/{stop_number}/schedule'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('invalid_stop', system,
            stop_number=stop_number
        )
    return page('stop/schedule', system,
        title=f'Stop {stop.number}',
        enable_refresh=False,
        stop=stop
    )

@endpoint('/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>')
def stop_schedule_date_page(system, stop_number, date_string):
    if system is None:
        return error_page('system_required', system,
            path=f'stops/{stop_number}/schedule'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('invalid_stop', system,
            stop_number=stop_number
        )
    date = Date.parse_db(date_string, None)
    return page('stop/date', system,
        title=f'Stop {stop.number}',
        enable_refresh=False,
        stop=stop,
        date=date
    )

@endpoint('/about')
def about_page(system):
    return page('about', system,
        title='About',
        enable_refresh=False,
        path='about'
    )

@endpoint('/nearby')
def nearby_page(system):
    return page('nearby', system,
        title='Nearby Stops',
        path='nearby',
        include_maps=True)

@endpoint('/themes')
def themes_page(system):
    redirect(get_url(system, 'personalize'))

@endpoint('/personalize')
def themes_page(system):
    theme_id = request.query.get('theme')
    if theme_id is not None:
        set_cookie('theme', theme_id)
    time_format = request.query.get('time_format')
    if time_format is not None:
        set_cookie('time_format', time_format)
    bus_marker_style = request.query.get('bus_marker_style')
    if bus_marker_style is not None:
        set_cookie('bus_marker_style', bus_marker_style)
    themes = helpers.theme.find_all()
    return page('personalize', system,
        title='Personalize',
        enable_refresh=False,
        path='personalize',
        themes=themes
    )

@endpoint('/systems')
def systems_page(system):
    return page('systems', system,
        title='Systems',
        enable_refresh=False,
        path=request.query.get('path', '')
    )

@endpoint('/admin')
def admin_page(system):
    return make_admin_key_page(system, None)

@endpoint('/admin/<key>')
def admin_key_page(system, key):
    return make_admin_key_page(system, key)

def make_admin_key_page(system, key):
    if admin_key is None or key == admin_key:
        if key is None:
            path = 'admin'
        else:
            path = f'admin/{key}'
        return page('admin', system,
            title='Administration',
            enable_refresh=False,
            path=path,
            key=key,
            disable_indexing=True
        )
    return page('home', system,
        title='Home',
        enable_refresh=False
    )

# =============================================================
# Frames
# =============================================================

@endpoint('/frame/nearby', append_slash=False)
def frame_nearby(system):
    if system is None:
        response.status = 400
        return None
    stops = sorted(system.get_stops())
    lat = float(request.query.get('lat'))
    lon = float(request.query.get('lon'))
    return frame('nearby', system,
        stops=sorted([s for s in stops if s.is_near(lat, lon)])
    )

# =============================================================
# API endpoints
# =============================================================

@endpoint('/api/health-check', append_slash=False)
def api_health_check(system):
    return 'Online'

@endpoint('/api/map.json', append_slash=False)
def api_map(system):
    time_format = request.get_cookie('time_format')
    if system is None:
        last_updated = realtime.get_last_updated(time_format)
    else:
        last_updated = system.get_last_updated(time_format)
    positions = sorted(helpers.position.find_all(system, has_location=True), key=lambda p: p.lat, reverse=True)
    return {
        'positions': [p.get_json() for p in positions],
        'last_updated': last_updated
    }

@endpoint('/api/shape/<shape_id>.json', append_slash=False)
def api_shape_id(system, shape_id):
    return {
        'points': [p.get_json() for p in helpers.point.find_all(system, shape_id)]
    }

@endpoint('/api/search', method='POST')
def api_search(system):
    query = request.forms.get('query', '')
    matches = []
    if query != '':
        if query.isnumeric() and (system is None or system.realtime_enabled):
            matches += helpers.order.find_matches(query, helpers.overview.find_bus_numbers(system))
        if system is not None:
            matches += system.search_blocks(query)
            matches += system.search_routes(query)
            matches += system.search_stops(query)
    matches = sorted([m for m in matches if m.value > 0])
    return {
        'results': [m.get_json(system, get_url) for m in matches[0:10]],
        'count': len(matches)
    }

@endpoint('/api/nearby.json', append_slash=False)
def api_nearby(system):
    if system is None:
        return {
            'stops': []
        }
    lat = float(request.query.get('lat'))
    lon = float(request.query.get('lon'))
    stops = sorted([s for s in system.get_stops() if s.is_near(lat, lon)])
    return {
        'stops': [s.get_json() for s in stops]
    }

@endpoint('/api/admin/reload-adornments', method='POST')
def api_admin_reload_adornments(system):
    return execute_api_admin_reload_adornments(None)

@endpoint('/api/admin/<key>/reload-adornments', method='POST')
def api_admin_key_reload_adornments(system, key):
    return execute_api_admin_reload_adornments(key)

def execute_api_admin_reload_adornments(key):
    if admin_key is None or key == admin_key:
        helpers.adornment.delete_all()
        helpers.adornment.load()
        return 'Success'
    return 'Access denied'

@endpoint('/api/admin/reload-orders', method='POST')
def api_admin_reload_orders(system):
    return execute_api_admin_reload_orders(None)

@endpoint('/api/admin/<key>/reload-orders', method='POST')
def api_admin_key_reload_orders(system, key):
    return execute_api_admin_reload_orders(key)

def execute_api_admin_reload_orders(key):
    if admin_key is None or key == admin_key:
        helpers.model.delete_all()
        helpers.order.delete_all()
        helpers.model.load()
        helpers.order.load()
        return 'Success'
    return 'Access denied'

@endpoint('/api/admin/reload-systems', method='POST')
def api_admin_reload_systems(system):
    return execute_api_admin_reload_systems(None)

@endpoint('/api/admin/<key>/reload-systems', method='POST')
def api_admin_key_reload_systems(system, key):
    return execute_api_admin_reload_systems(key)

def execute_api_admin_reload_systems(key):
    if admin_key is None or key == admin_key:
        cron.stop(cron_id)
        helpers.region.delete_all()
        helpers.system.delete_all()
        helpers.position.delete_all()
        helpers.region.load()
        helpers.system.load()
        for system in helpers.system.find_all():
            if running:
                gtfs.load(system)
                if not gtfs.validate(system):
                    gtfs.load(system, True)
                gtfs.update_cache_in_background(system)
                realtime.update(system)
                if not realtime.validate(system):
                    system.validation_errors += 1
        if running:
            realtime.update_records()
            cron.start(cron_id)
        return 'Success'
    return 'Access denied'

@endpoint('/api/admin/reload-themes', method='POST')
def api_admin_reload_themes(system):
    return execute_api_admin_reload_themes(None)

@endpoint('/api/admin/<key>/reload-themes', method='POST')
def api_admin_key_reload_themes(system, key):
    return execute_api_admin_reload_themes(key)

def execute_api_admin_reload_themes(key):
    if admin_key is None or key == admin_key:
        helpers.theme.delete_all()
        helpers.theme.load()
        return 'Success'
    return 'Access denied'

@endpoint('/api/admin/restart-cron', method='POST')
def api_admin_restart_cron(system):
    return execute_api_admin_restart_cron(None)

@endpoint('/api/admin/<key>/restart-cron', method='POST')
def api_admin_key_restart_cron(system, key):
    return execute_api_admin_restart_cron(key)

def execute_api_admin_restart_cron(key):
    if admin_key is None or key == admin_key:
        cron.stop(cron_id)
        cron.start(cron_id)
        return 'Success'
    return 'Access denied'

@endpoint('/api/admin/backup-database', method='POST')
def api_admin_backup_database(system):
    return execute_api_admin_backup_database(None)

@endpoint('/api/admin/<key>/backup-database', method='POST')
def api_admin_key_backup_database(system, key):
    return execute_api_admin_backup_database(key)

def execute_api_admin_backup_database(key):
    if admin_key is None or key == admin_key:
        database.archive()
        return 'Success'
    return 'Access denied'

@endpoint('/api/admin/reload-gtfs/<reload_system_id>', method='POST')
def api_admin_reload_gtfs(system, reload_system_id):
    return execute_api_admin_reload_gtfs(None, reload_system_id)

@endpoint('/api/admin/<key>/reload-gtfs/<reload_system_id>', method='POST')
def api_admin_key_reload_gtfs(system, key, reload_system_id):
    return execute_api_admin_reload_gtfs(key, reload_system_id)

def execute_api_admin_reload_gtfs(key, reload_system_id):
    if admin_key is None or key == admin_key:
        system = helpers.system.find(reload_system_id)
        if system is None:
            return 'Invalid system'
        gtfs.load(system, True)
        gtfs.update_cache_in_background(system)
        realtime.update(system)
        if not realtime.validate(system):
            system.validation_errors += 1
        realtime.update_records()
        return 'Success'
    return 'Access denied'

@endpoint('/api/admin/reload-realtime/<reload_system_id>', method='POST')
def api_admin_reload_realtime(system, reload_system_id):
    return execute_api_admin_reload_realtime(None, reload_system_id)

@endpoint('/api/admin/<key>/reload-realtime/<reload_system_id>', method='POST')
def api_admin_key_reload_realtime(system, key, reload_system_id):
    return execute_api_admin_reload_realtime(key, reload_system_id)

def execute_api_admin_reload_realtime(key, reload_system_id):
    if admin_key is None or key == admin_key:
        system = helpers.system.find(reload_system_id)
        if system is None:
            return 'Invalid system'
        realtime.update(system)
        if not realtime.validate(system):
            system.validation_errors += 1
        realtime.update_records()
        return 'Success'
    return 'Access denied'

# =============================================================
# Errors
# =============================================================

@app.error(404)
def error_404_page(error):
    return error_page('404', None, error=error)

@app.error(500)
def error_500_page(error):
    return error_page('500', None, error=error)
