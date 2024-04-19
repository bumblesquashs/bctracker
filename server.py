
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, HTTPError, static_file, template, request, response, debug, redirect
from datetime import timedelta
import cherrypy as cp

import helpers.adornment
import helpers.agency
import helpers.model
import helpers.order
import helpers.overview
import helpers.point
import helpers.position
import helpers.record
import helpers.region
import helpers.route
import helpers.stop
import helpers.system
import helpers.theme
import helpers.transfer
import helpers.assignment

from models.bus import Bus
from models.date import Date
from models.event import Event
from models.favourite import Favourite, FavouriteSet

import config
import cron
import database
import gtfs
import realtime

# Increase the version to force CSS reload
VERSION = 36

app = Bottle()
running = False

def start(args):
    '''Loads all required data and launches the server'''
    global running
    
    cp.config.update('server.conf')
    config.setup(cp.config)
    
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
    helpers.order.load()
    helpers.system.load()
    helpers.theme.load()
    
    helpers.position.delete_all()
    
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
        cron.start()

def stop():
    '''Terminates the server'''
    global running
    running = False
    cron.stop()
    database.disconnect()
    if cp.server.running:
        cp.server.stop()

def get_url(system, path='', **kwargs):
    '''Returns a URL formatted based on the given system and path'''
    system_id = getattr(system, 'id', system)
    if system_id:
        url = config.system_domain.format(system_id, path).rstrip('/')
    else:
        url = config.all_systems_domain.format(path).rstrip('/')
    query_args = {k:v for k, v in kwargs.items() if v is not None}
    if query_args:
        query = '&'.join([f'{k}={v}' for k, v in query_args.items()])
        url += f'?{query}'
    return url

def validate_admin():
    '''Checks if the admin key in the query/cookie matches the expected admin key'''
    return not config.admin_key or query_cookie('admin_key', max_age_days=1) == config.admin_key

def page(name, title, path='', path_args=None, system=None, agency=None, enable_refresh=True, include_maps=False, full_map=False, **kwargs):
    '''Returns an HTML page with the given name and details'''
    is_admin = validate_admin()
    
    theme_id = request.query.get('theme') or request.get_cookie('theme')
    time_format = request.query.get('time_format') or request.get_cookie('time_format')
    bus_marker_style = request.query.get('bus_marker_style') or request.get_cookie('bus_marker_style')
    hide_systems = request.get_cookie('hide_systems') == 'yes'
    try:
        last_updated = system.get_last_updated(time_format)
    except AttributeError:
        last_updated = realtime.get_last_updated(time_format)
    return template(f'pages/{name}',
        config=config,
        version=VERSION,
        title=title,
        path=path,
        path_args=path_args or {},
        system=system,
        agency=agency,
        enable_refresh=enable_refresh,
        include_maps=include_maps,
        full_map=full_map,
        regions=helpers.region.find_all(),
        systems=helpers.system.find_all(),
        is_admin=is_admin,
        get_url=get_url,
        last_updated=last_updated,
        theme=helpers.theme.find(theme_id),
        time_format=time_format,
        bus_marker_style=bus_marker_style,
        hide_systems=hide_systems,
        show_speed=request.get_cookie('speed') == '1994',
        **kwargs
    )

def error_page(name, title, path='', path_args=None, system=None, agency=None, **kwargs):
    '''Returns an error page with the given name and details'''
    return page(
        name=f'errors/{name}',
        title=title,
        path=path,
        path_args=path_args,
        system=system,
        agency=agency,
        enable_refresh=False,
        **kwargs
    )

def frame(name, system, agency, **kwargs):
    return template(f'frames/{name}',
        system=system,
        agency=agency,
        get_url=get_url,
        time_format=request.get_cookie('time_format'),
        show_speed=request.get_cookie('speed') == '1994',
        **kwargs
    )

def set_cookie(key, value, max_age_days=3650):
    '''Creates a cookie using the given key and value'''
    max_age = 60 * 60 * 24 * max_age_days
    if config.cookie_domain:
        response.set_cookie(key, value, max_age=max_age, domain=config.cookie_domain, path='/')
    else:
        response.set_cookie(key, value, max_age=max_age, path='/')

def query_cookie(key, default_value=None, max_age_days=3650):
    '''Creates a cookie if a query value exists, otherwise uses the existing cookie value'''
    value = request.query.get(key)
    if value is not None:
        set_cookie(key, value, max_age_days)
        return value
    return request.get_cookie(key, default_value)

def get_favourites():
    '''Returns the current set of favourites stored in the cookie'''
    favourites_string = request.get_cookie('favourites', '')
    return FavouriteSet.parse(favourites_string)

def endpoint(base_path, method='GET', append_slash=True, require_admin=False, system_key='system_id'):
    def endpoint_wrapper(func):
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
        @app.route(paths, method)
        def func_wrapper(*args, **kwargs):
            if require_admin and not validate_admin():
                raise HTTPError(403)
            if system_key in kwargs:
                system_id = kwargs[system_key]
                system = helpers.system.find(system_id)
                if not system:
                    raise HTTPError(404)
                del kwargs[system_key]
            else:
                system = None
            agency = helpers.agency.find('bc-transit')
            return func(system=system, agency=agency, *args, **kwargs)
        return func_wrapper
    return endpoint_wrapper

# =============================================================
# Static Files
# =============================================================

@endpoint('/style/<name:path>', append_slash=False)
def style(system, agency, name):
    return static_file(name, root='./style')

@endpoint('/img/<name:path>', append_slash=False)
def img(system, agency, name):
    return static_file(name, root='./img')

@endpoint('/js/<name:path>', append_slash=False)
def img(system, agency, name):
    return static_file(name, root='./js')

@endpoint('/robots.txt', append_slash=False)
def robots_text(system, agency):
    return static_file('robots.txt', root='.')

# =============================================================
# Pages
# =============================================================

@endpoint('/')
def home_page(system, agency):
    return page(
        name='home',
        title='Home',
        system=system,
        agency=agency,
        enable_refresh=False,
        favourites=get_favourites()
    )

@endpoint('/news')
def news_page(system, agency):
    return page(
        name='news',
        title='News Archive',
        path='news',
        system=system,
        agency=agency,
        enable_refresh=False
    )

@endpoint('/map')
def map_page(system, agency):
    positions = helpers.position.find_all(system, has_location=True)
    auto_refresh = query_cookie('auto_refresh', 'false') != 'false'
    show_route_lines = query_cookie('show_route_lines', 'false') != 'false'
    show_nis = query_cookie('show_nis', 'true') != 'false'
    visible_positions = positions if show_nis else [p for p in positions if p.trip]
    return page(
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

@endpoint('/realtime')
def realtime_all_page(system, agency):
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip]
    return page(
        name='realtime/all',
        title='Realtime',
        path='realtime',
        system=system,
        agency=agency,
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/realtime/routes')
def realtime_routes_page(system, agency):
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip]
    return page(
        name='realtime/routes',
        title='Realtime',
        path='realtime/routes',
        system=system,
        agency=agency,
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/realtime/models')
def realtime_models_page(system, agency):
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip]
    return page(
        name='realtime/models',
        title='Realtime',
        path='realtime/models',
        system=system,
        agency=agency,
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/realtime/speed')
def realtime_speed_page(system, agency):
    set_cookie('speed', '1994')
    positions = helpers.position.find_all(system)
    show_nis = query_cookie('show_nis', 'true') != 'false'
    if not show_nis:
        positions = [p for p in positions if p.trip]
    return page(
        name='realtime/speed',
        title='Realtime',
        path='realtime/speed',
        system=system,
        agency=agency,
        positions=positions,
        show_nis=show_nis
    )

@endpoint('/fleet')
def fleet_page(system, agency):
    orders = helpers.order.find_all(agency)
    overviews = helpers.overview.find_all()
    return page(
        name='fleet',
        title='Fleet',
        path='fleet',
        system=system,
        agency=agency,
        orders=[o for o in sorted(orders) if o.visible],
        overviews={o.bus.number: o for o in overviews}
    )

@endpoint('/bus/<bus_number:int>')
def bus_overview_page(system, agency, bus_number):
    bus = Bus.find(agency, bus_number)
    overview = helpers.overview.find(bus)
    if (not bus.order and not overview) or not bus.visible:
        return error_page(
            name='invalid_bus',
            title='Unknown Bus',
            system=system,
            agency=agency,
            bus_number=bus_number
        )
    position = helpers.position.find(bus)
    records = helpers.record.find_all(bus=bus, limit=20)
    return page(
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
        favourites=get_favourites()
    )

@endpoint('/bus/<bus_number:int>/map')
def bus_map_page(system, agency, bus_number):
    bus = Bus.find(agency, bus_number)
    overview = helpers.overview.find(bus)
    if (not bus.order and not overview) or not bus.visible:
        return error_page(
            name='invalid_bus',
            title='Unknown Bus',
            system=system,
            agency=agency,
            bus_number=bus_number
        )
    position = helpers.position.find(bus)
    return page(
        name='bus/map',
        title=f'Bus {bus}',
        system=system,
        agency=agency,
        include_maps=bool(position),
        full_map=bool(position),
        bus=bus,
        position=position,
        favourite=Favourite('vehicle', bus),
        favourites=get_favourites()
    )

@endpoint('/bus/<bus_number:int>/history')
def bus_history_page(system, agency, bus_number):
    bus = Bus.find(agency, bus_number)
    overview = helpers.overview.find(bus)
    if (not bus.order and not overview) or not bus.visible:
        return error_page(
            name='invalid_bus',
            title='Unknown Bus',
            system=system,
            agency=agency,
            bus_number=bus_number
        )
    records = helpers.record.find_all(bus=bus)
    transfers = helpers.transfer.find_all(bus=bus)
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
    return page(
        name='bus/history',
        title=f'Bus {bus}',
        system=system,
        agency=agency,
        bus=bus,
        records=records,
        overview=overview,
        events=events,
        favourite=Favourite('vehicle', bus),
        favourites=get_favourites()
    )

@endpoint('/history')
def history_last_seen_page(system, agency):
    overviews = [o for o in helpers.overview.find_all(system) if o.last_record and o.bus.visible]
    try:
        days = int(request.query['days'])
    except ValueError:
        days = None
    if days:
        try:
            date = Date.today(system.timezone) - timedelta(days=days)
        except AttributeError:
            date = Date.today() - timedelta(days=days)
        overviews = [o for o in overviews if o.last_record.date > date]
    return page(
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

@endpoint('/history/first-seen')
def history_first_seen_page(system, agency):
    overviews = [o for o in helpers.overview.find_all(system) if o.first_record and o.bus.visible]
    return page(
        name='history/first_seen',
        title='Vehicle History',
        path='history/first-seen',
        system=system,
        agency=agency,
        overviews=sorted(overviews, key=lambda o: (o.first_record.date, o.first_record.first_seen, o.bus), reverse=True)
    )

@endpoint('/history/transfers')
def history_transfers_page(system, agency):
    transfers = helpers.transfer.find_all(system)
    return page(
        name='history/transfers',
        title='Vehicle History',
        path='history/transfers',
        system=system,
        agency=agency,
        transfers=[t for t in transfers if t.bus.visible]
    )

@endpoint('/routes')
def routes_list_page(system, agency):
    return page(
        name='routes/list',
        title='Routes',
        path='routes',
        system=system,
        agency=agency,
        enable_refresh=False
    )

@endpoint('/routes/map')
def routes_map_page(system, agency):
    routes = helpers.route.find_all(system)
    show_route_numbers = query_cookie('show_route_numbers', 'true') != 'false'
    return page(
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

@endpoint('/routes/<route_number>')
def route_overview_page(system, agency, route_number):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'routes/{route_number}',
            system=system,
            agency=agency
        )
    route = system.get_route(number=route_number)
    if not route:
        return error_page(
            name='invalid_route',
            title='Unknown Route',
            system=system,
            agency=agency,
            route_number=route_number
        )
    trips = sorted(route.get_trips(date=Date.today(system.timezone)))
    return page(
        name='route/overview',
        title=str(route),
        system=system,
        agency=agency,
        include_maps=len(route.trips) > 0,
        route=route,
        trips=trips,
        recorded_today=helpers.record.find_recorded_today(system, trips),
        assignments=helpers.assignment.find_all(system, route=route),
        positions=helpers.position.find_all(system, route=route),
        favourite=Favourite('route', route),
        favourites=get_favourites()
    )

@endpoint('/routes/<route_number>/map')
def route_map_page(system, agency, route_number):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'routes/{route_number}/map',
            system=system,
            agency=agency
        )
    route = system.get_route(number=route_number)
    if not route:
        return error_page(
            name='invalid_route',
            title='Unknown Route',
            system=system,
            agency=agency,
            route_number=route_number
        )
    return page(
        name='route/map',
        title=str(route),
        system=system,
        agency=agency,
        include_maps=len(route.trips) > 0,
        full_map=len(route.trips) > 0,
        route=route,
        positions=helpers.position.find_all(system, route=route),
        favourite=Favourite('route', route),
        favourites=get_favourites()
    )

@endpoint('/routes/<route_number>/schedule')
def route_schedule_page(system, agency, route_number):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'routes/{route_number}/schedule',
            system=system,
            agency=agency
        )
    route = system.get_route(number=route_number)
    if not route:
        return error_page(
            name='invalid_route',
            title='Unknown Route',
            system=system,
            agency=agency,
            route_number=route_number
        )
    return page(
        name='route/schedule',
        title=str(route),
        system=system,
        agency=agency,
        enable_refresh=False,
        route=route,
        favourite=Favourite('route', route),
        favourites=get_favourites()
    )

@endpoint('/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>')
def route_schedule_date_page(system, agency, route_number, date_string):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'routes/{route_number}/schedule',
            system=system,
            agency=agency
        )
    route = system.get_route(number=route_number)
    if not route:
        return error_page(
            name='invalid_route',
            title='Unknown Route',
            system=system,
            agency=agency,
            route_number=route_number
        )
    date = Date.parse(date_string, system.timezone)
    return page(
        name='route/date',
        title=str(route),
        system=system,
        agency=agency,
        enable_refresh=False,
        route=route,
        date=date,
        favourite=Favourite('route', route),
        favourites=get_favourites()
    )

@endpoint('/blocks')
def blocks_page(system, agency):
    return page(
        name='blocks/list',
        title='Blocks',
        path='blocks',
        system=system,
        agency=agency,
        enable_refresh=False
    )

@endpoint('/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>')
def blocks_schedule_date_page(system, agency, date_string):
    try:
        date = Date.parse(date_string, system.timezone)
    except AttributeError:
        date = Date.parse(date_string)
    return page(
        name='blocks/date',
        title='Blocks',
        path=f'blocks/schedule/{date_string}',
        system=system,
        agency=agency,
        enable_reload=False,
        date=date
    )

@endpoint('/blocks/<block_id>')
def block_overview_page(system, agency, block_id):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'blocks/{block_id}',
            system=system,
            agency=agency
        )
    block = system.get_block(block_id)
    if not block:
        return error_page(
            name='invalid_block',
            title='Unknown Block',
            system=system,
            agency=agency,
            block_id=block_id
        )
    return page(
        name='block/overview',
        title=f'Block {block.id}',
        system=system,
        agency=agency,
        include_maps=True,
        block=block,
        positions=helpers.position.find_all(system, block=block),
        assignment=helpers.assignment.find(system, block)
    )

@endpoint('/blocks/<block_id>/map')
def block_map_page(system, agency, block_id):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'blocks/{block_id}/map',
            system=system,
            agency=agency
        )
    block = system.get_block(block_id)
    if not block:
        return error_page(
            name='invalid_block',
            title='Unknown Block',
            system=system,
            agency=agency,
            block_id=block_id
        )
    return page(
        name='block/map',
        title=f'Block {block.id}',
        system=system,
        agency=agency,
        include_maps=True,
        full_map=True,
        block=block,
        positions=helpers.position.find_all(system, block=block)
    )

@endpoint('/blocks/<block_id>/history')
def block_history_page(system, agency, block_id):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'blocks/{block_id}/history',
            system=system,
            agency=agency
        )
    block = system.get_block(block_id)
    if not block:
        return error_page(
            name='invalid_block',
            title='Unknown Block',
            system=system,
            agency=agency,
            block_id=block_id
        )
    records = helpers.record.find_all(system, block=block)
    events = []
    if records:
        events.append(Event(records[0].date, 'Last Tracked'))
        events.append(Event(records[-1].date, 'First Tracked'))
    return page(
        name='block/history',
        title=f'Block {block.id}',
        system=system,
        agency=agency,
        block=block,
        records=records,
        events=events
    )

@endpoint('/trips/<trip_id>')
def trip_overview_page(system, agency, trip_id):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'trips/{trip_id}',
            system=system,
            agency=agency
        )
    trip = system.get_trip(trip_id)
    if not trip:
        return error_page(
            name='invalid_trip',
            title='Unknown Trip',
            system=system,
            agency=agency,
            trip_id=trip_id
        )
    return page(
        name='trip/overview',
        title=f'Trip {trip.id}',
        system=system,
        agency=agency,
        include_maps=True,
        trip=trip,
        positions=helpers.position.find_all(system, trip=trip),
        assignment=helpers.assignment.find(system, trip.block_id)
    )

@endpoint('/trips/<trip_id>/map')
def trip_map_page(system, agency, trip_id):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'trips/{trip_id}/map',
            system=system,
            agency=agency
        )
    trip = system.get_trip(trip_id)
    if not trip:
        return error_page(
            name='invalid_trip',
            title='Unknown Trip',
            system=system,
            agency=agency,
            trip_id=trip_id
        )
    return page(
        name='trip/map',
        title=f'Trip {trip.id}',
        system=system,
        agency=agency,
        include_maps=True,
        full_map=True,
        trip=trip,
        positions=helpers.position.find_all(system, trip=trip)
    )

@endpoint('/trips/<trip_id>/history')
def trip_history_page(system, agency, trip_id):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'trips/{trip_id}/history',
            system=system,
            agency=agency
        )
    trip = system.get_trip(trip_id)
    if not trip:
        return error_page(
            name='invalid_trip',
            title='Unknown Trip',
            system=system,
            agency=agency,
            trip_id=trip_id
        )
    records = helpers.record.find_all(system, trip=trip)
    events = []
    if len(records) > 0:
        events.append(Event(records[0].date, 'Last Tracked'))
        events.append(Event(records[-1].date, 'First Tracked'))
    return page(
        name='trip/history',
        title=f'Trip {trip.id}',
        system=system,
        agency=agency,
        trip=trip,
        records=records,
        events=events
    )

@endpoint('/stops')
def stops_page(system, agency):
    path_args = {}
    search = request.query.get('search')
    if search:
        path_args['search'] = search
    return page(
        name='stops',
        title='Stops',
        path='stops',
        path_args=path_args,
        system=system,
        agency=agency,
        enable_refresh=False,
        search=search
    )

@endpoint('/stops/<stop_number>')
def stop_overview_page(system, agency, stop_number):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'stops/{stop_number}',
            system=system,
            agency=agency
        )
    stop = system.get_stop(number=stop_number)
    if not stop:
        return error_page(
            name='invalid_stop',
            title='Unknown Stop',
            system=system,
            agency=agency,
            stop_number=stop_number
        )
    departures = stop.find_departures(date=Date.today(system.timezone))
    trips = [d.trip for d in departures]
    positions = helpers.position.find_all(system, trip=trips)
    return page(
        name='stop/overview',
        title=f'Stop {stop.number}',
        system=system,
        agency=agency,
        include_maps=True,
        stop=stop,
        departures=departures,
        recorded_today=helpers.record.find_recorded_today(system, trips),
        assignments=helpers.assignment.find_all(system, stop=stop),
        positions={p.trip.id: p for p in positions},
        favourite=Favourite('stop', stop),
        favourites=get_favourites()
    )

@endpoint('/stops/<stop_number>/map')
def stop_map_page(system, agency, stop_number):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'stops/{stop_number}/map',
            system=system,
            agency=agency
        )
    stop = system.get_stop(number=stop_number)
    if not stop:
        return error_page(
            name='invalid_stop',
            title='Unknown Stop',
            system=system,
            agency=agency,
            stop_number=stop_number
        )
    return page(
        name='stop/map',
        title=f'Stop {stop.number}',
        system=system,
        agency=agency,
        include_maps=True,
        full_map=True,
        stop=stop,
        favourite=Favourite('stop', stop),
        favourites=get_favourites()
    )

@endpoint('/stops/<stop_number>/schedule')
def stop_schedule_page(system, agency, stop_number):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'stops/{stop_number}/schedule',
            system=system,
            agency=agency
        )
    stop = system.get_stop(number=stop_number)
    if not stop:
        return error_page(
            name='invalid_stop',
            title='Unknown Stop',
            system=system,
            agency=agency,
            stop_number=stop_number
        )
    return page(
        name='stop/schedule',
        title=f'Stop {stop.number}',
        system=system,
        agency=agency,
        enable_refresh=False,
        stop=stop,
        favourite=Favourite('stop', stop),
        favourites=get_favourites()
    )

@endpoint('/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>')
def stop_schedule_date_page(system, agency, stop_number, date_string):
    if not system:
        return error_page(
            name='system_required',
            title='System Required',
            path=f'stops/{stop_number}/schedule',
            system=system,
            agency=agency
        )
    stop = system.get_stop(number=stop_number)
    if not stop:
        return error_page(
            name='invalid_stop',
            title='Unknown Stop',
            system=system,
            agency=agency,
            stop_number=stop_number
        )
    date = Date.parse(date_string, system.timezone)
    return page(
        name='stop/date',
        title=f'Stop {stop.number}',
        system=system,
        agency=agency,
        enable_refresh=False,
        stop=stop,
        date=date,
        favourite=Favourite('stop', stop),
        favourites=get_favourites()
    )

@endpoint('/about')
def about_page(system, agency):
    return page(
        name='about',
        title='About',
        path='about',
        system=system,
        agency=agency,
        enable_refresh=False
    )

@endpoint('/nearby')
def nearby_page(system, agency):
    return page(
        name='nearby',
        title='Nearby Stops',
        path='nearby',
        system=system,
        agency=agency,
        include_maps=True
    )

@endpoint('/themes')
def themes_page(system, agency):
    redirect(get_url(system, 'personalize'))

@endpoint('/personalize')
def personalize_page(system, agency):
    theme_id = request.query.get('theme')
    if theme_id:
        set_cookie('theme', theme_id)
    time_format = request.query.get('time_format')
    if time_format:
        set_cookie('time_format', time_format)
    bus_marker_style = request.query.get('bus_marker_style')
    if bus_marker_style:
        set_cookie('bus_marker_style', bus_marker_style)
    themes = helpers.theme.find_all()
    return page(
        name='personalize',
        title='Personalize',
        path='personalize',
        system=system,
        agency=agency,
        enable_refresh=False,
        themes=themes
    )

@endpoint('/systems')
def systems_page(system, agency):
    return page(
        name='systems',
        title='Systems',
        path=request.query.get('path', ''),
        system=system,
        agency=agency,
        enable_refresh=False
    )

@endpoint('/admin', require_admin=True)
def admin_page(system, agency):
    return page(
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

@endpoint('/frame/nearby', append_slash=False)
def frame_nearby(system, agency):
    if not system:
        response.status = 400
        return None
    stops = sorted(system.get_stops())
    lat = float(request.query.get('lat'))
    lon = float(request.query.get('lon'))
    return frame(
        name='nearby',
        system=system,
        agency=agency,
        stops=sorted([s for s in stops if s.is_near(lat, lon)])
    )

# =============================================================
# API endpoints
# =============================================================

@endpoint('/api/health-check', append_slash=False)
def api_health_check(system, agency):
    return 'Online'

@endpoint('/api/map.json', append_slash=False)
def api_map(system, agency):
    time_format = request.get_cookie('time_format')
    try:
        last_updated = system.get_last_updated(time_format)
    except AttributeError:
        last_updated = realtime.get_last_updated(time_format)
    positions = sorted(helpers.position.find_all(system, has_location=True), key=lambda p: p.lat)
    return {
        'positions': [p.get_json() for p in positions],
        'last_updated': last_updated
    }

@endpoint('/api/shape/<shape_id>.json', append_slash=False)
def api_shape_id(system, agency, shape_id):
    return {
        'points': [p.get_json() for p in helpers.point.find_all(system, shape_id)]
    }

@endpoint('/api/routes')
def api_routes(system, agency):
    routes = helpers.route.find_all(system)
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

@endpoint('/api/search', method='POST')
def api_search(system, agency):
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
                matches += helpers.order.find_matches(agency, query, helpers.overview.find_bus_numbers(system))
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
        'results': [m.get_json(system, get_url) for m in matches[min:max]],
        'total': len(matches)
    }

@endpoint('/api/nearby.json', append_slash=False)
def api_nearby(system, agency):
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

@endpoint('/api/admin/reload-adornments', method='POST', require_admin=True)
def api_admin_reload_adornments(system, agency):
    helpers.adornment.load()
    return 'Success'

@endpoint('/api/admin/reload-orders', method='POST', require_admin=True)
def api_admin_reload_orders(system, agency):
    helpers.order.load()
    return 'Success'

@endpoint('/api/admin/reload-systems', method='POST', require_admin=True)
def api_admin_reload_systems(system, agency):
    cron.stop()
    helpers.position.delete_all()
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
        cron.start()
    return 'Success'

@endpoint('/api/admin/reload-themes', method='POST', require_admin=True)
def api_admin_reload_themes(system, agency):
    helpers.theme.load()
    return 'Success'

@endpoint('/api/admin/restart-cron', method='POST', require_admin=True)
def api_admin_restart_cron(system, agency):
    cron.stop()
    cron.start()
    return 'Success'

@endpoint('/api/admin/backup-database', method='POST', require_admin=True)
def api_admin_backup_database(system, agency):
    database.archive()
    return 'Success'

@endpoint('/api/admin/reload-gtfs/<reload_system_id>', method='POST', require_admin=True)
def api_admin_reload_gtfs(system, agency, reload_system_id):
    system = helpers.system.find(reload_system_id)
    if not system:
        return 'Invalid system'
    gtfs.load(system, True)
    gtfs.update_cache_in_background(system)
    realtime.update(system)
    if not realtime.validate(system):
        system.validation_errors += 1
    realtime.update_records()
    return 'Success'

@endpoint('/api/admin/reload-realtime/<reload_system_id>', method='POST', require_admin=True)
def api_admin_reload_realtime(system, agency, reload_system_id):
    system = helpers.system.find(reload_system_id)
    if not system:
        return 'Invalid system'
    realtime.update(system)
    if not realtime.validate(system):
        system.validation_errors += 1
    realtime.update_records()
    return 'Success'

# =============================================================
# Errors
# =============================================================

@app.error(403)
def error_403_page(error):
    return error_page('403', None, 'Forbidden', error=error)

@app.error(404)
def error_404_page(error):
    return error_page('404', None, 'Not Found', error=error)

@app.error(500)
def error_500_page(error):
    return error_page('500', None, 'Internal Error', error=error)
