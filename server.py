
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, static_file, template, request, response, debug, redirect
import cherrypy as cp

import helpers.adornment
import helpers.model
import helpers.order
import helpers.overview
import helpers.point
import helpers.position
import helpers.record
import helpers.region
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
VERSION = 18

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
    if system is None:
        url = no_system_domain.format(path).rstrip('/')
    elif isinstance(system, str):
        url = system_domain.format(system, path).rstrip('/')
    else:
        url = system_domain.format(system.id, path).rstrip('/')
    if len(kwargs) > 0:
        query = '&'.join([f'{k}={v}' for k, v in kwargs.items() if v is not None])
        url += f'?{query}'
    return url

def page(name, system_id, title, path='', enable_refresh=True, include_maps=False, full_map=False, **kwargs):
    '''Returns an HTML page with the given name and details'''
    theme_id = request.query.get('theme') or request.get_cookie('theme')
    time_format = request.query.get('time_format') or request.get_cookie('time_format')
    hide_systems = request.get_cookie('hide_systems') == 'yes'
    system = helpers.system.find(system_id)
    if system is None:
        last_updated = realtime.get_last_updated(time_format)
    else:
        last_updated = system.get_last_updated(time_format)
    return template(f'pages/{name}',
        version=VERSION,
        title=title,
        path=path,
        enable_refresh=enable_refresh,
        include_maps=include_maps,
        full_map=full_map,
        regions=helpers.region.find_all(),
        systems=[s for s in helpers.system.find_all() if s.enabled and s.visible],
        admin_systems=helpers.system.find_all(),
        system_id=system_id,
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
        hide_systems=hide_systems,
        show_speed=request.get_cookie('speed') == '1994',
        **kwargs
    )

def error_page(name, system_id, title='Error', path='', **kwargs):
    '''Returns an error page with the given name and details'''
    return page(f'errors/{name}_error', system_id,
        title=title,
        path=path,
        enable_refresh=False,
        **kwargs
    )

def set_cookie(key, value):
    '''Creates a cookie using the given key and value'''
    max_age = 60*60*24*365*10
    if cookie_domain is None:
        response.set_cookie(key, value, max_age=max_age, path='/')
    else:
        response.set_cookie(key, value, max_age=max_age, domain=cookie_domain, path='/')

# =============================================================
# CSS (Static Files)
# =============================================================

@app.get([
    '/style/<name:path>',
    '/<system_id>/style/<name:path>'
])
def style(name, system_id=None):
    return static_file(name, root='./style')

# =============================================================
# Images (Static Files)
# =============================================================

@app.get([
    '/img/<name:path>',
    '/<system_id>/img/<name:path>'
])
def img(name, system_id=None):
    return static_file(name, root='./img')

# =============================================================
# HTML (Templates)
# =============================================================

@app.get([
    '/',
    '/<system_id>',
    '/<system_id>/'
])
def home_page(system_id=None):
    return page('home', system_id,
        title='Home',
        enable_refresh=False
    )

@app.get([
    '/news',
    '/news/',
    '/<system_id>/news',
    '/<system_id>/news/'
])
def news_page(system_id=None):
    return page('news', system_id,
        title='News Archive',
        path='news',
        enable_refresh=False
    )

@app.get([
    '/map',
    '/map/',
    '/<system_id>/map',
    '/<system_id>/map/'
])
def map_page(system_id=None):
    positions = helpers.position.find_all(system_id, has_location=True)
    return page('map', system_id,
        title='Map',
        path='map',
        include_maps=len(positions) > 0,
        full_map=len(positions) > 0,
        positions=sorted(positions, key=lambda p: p.lat, reverse=True)
    )

@app.get([
    '/realtime',
    '/realtime/',
    '/<system_id>/realtime',
    '/<system_id>/realtime/'
])
def realtime_all_page(system_id=None):
    return page('realtime/all', system_id,
        title='Realtime',
        path='realtime',
        positions=helpers.position.find_all(system_id)
    )

@app.get([
    '/realtime/routes',
    '/realtime/routes/',
    '/<system_id>/realtime/routes',
    '/<system_id>/realtime/routes/'
])
def realtime_routes_page(system_id=None):
    return page('realtime/routes', system_id,
        title='Realtime',
        path='realtime/routes',
        positions=helpers.position.find_all(system_id)
    )

@app.get([
    '/realtime/models',
    '/realtime/models/',
    '/<system_id>/realtime/models',
    '/<system_id>/realtime/models/'
])
def realtime_models_page(system_id=None):
    return page('realtime/models', system_id,
        title='Realtime',
        path='realtime/models',
        positions=helpers.position.find_all(system_id)
    )

@app.get([
    '/realtime/speed',
    '/realtime/speed/',
    '/<system_id>/realtime/speed',
    '/<system_id>/realtime/speed/'
])
def realtime_speed_page(system_id=None):
    set_cookie('speed', '1994')
    return page('realtime/speed', system_id,
        title='Realtime',
        path='realtime/speed',
        positions=helpers.position.find_all(system_id)
    )

@app.get([
    '/fleet',
    '/fleet/',
    '/<system_id>/fleet',
    '/<system_id>/fleet/'
])
def fleet_page(system_id=None):
    orders = helpers.order.find_all()
    overviews = helpers.overview.find_all()
    return page('fleet', system_id,
        title='Fleet',
        path='fleet',
        orders=[o for o in sorted(orders, key=lambda o: o.low) if not o.is_test],
        overviews={o.bus.number: o for o in overviews}
    )

@app.get([
    '/bus/<bus_number:int>',
    '/bus/<bus_number:int>/',
    '/<system_id>/bus/<bus_number:int>',
    '/<system_id>/bus/<bus_number:int>/'
])
def bus_overview_page(bus_number, system_id=None):
    bus = Bus(bus_number)
    overview = helpers.overview.find(bus_number)
    if (bus.order is None and overview is None) or bus.is_test:
        return error_page('bus', system_id,
            bus_number=bus_number
        )
    position = helpers.position.find(bus_number)
    records = helpers.record.find_all(bus_number=bus_number, limit=20)
    return page('bus/overview', system_id,
        title=f'Bus {bus}',
        include_maps=position is not None,
        bus=bus,
        position=position,
        records=records,
        overview=overview
    )

@app.get([
    '/bus/<bus_number:int>/map',
    '/bus/<bus_number:int>/map/',
    '/<system_id>/bus/<bus_number:int>/map',
    '/<system_id>/bus/<bus_number:int>/map/'
])
def bus_map_page(bus_number, system_id=None):
    bus = Bus(bus_number)
    overview = helpers.overview.find(bus_number)
    if (bus.order is None and overview is None) or bus.is_test:
        return error_page('bus', system_id,
            bus_number=bus_number
        )
    position = helpers.position.find(bus_number)
    return page('bus/map', system_id,
        title=f'Bus {bus}',
        include_maps=position is not None,
        full_map=position is not None,
        bus=bus,
        position=position
    )

@app.get([
    '/bus/<bus_number:int>/history',
    '/bus/<bus_number:int>/history/',
    '/<system_id>/bus/<bus_number:int>/history',
    '/<system_id>/bus/<bus_number:int>/history/'
])
def bus_history_page(bus_number, system_id=None):
    bus = Bus(bus_number)
    overview = helpers.overview.find(bus_number)
    if (bus.order is None and overview is None) or bus.is_test:
        return error_page('bus', system_id,
            bus_number=bus_number
        )
    records = helpers.record.find_all(bus_number=bus_number)
    transfers = helpers.transfer.find_all(bus_number=bus_number)
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
    return page('bus/history', system_id,
        title=f'Bus {bus}',
        bus=bus,
        records=records,
        overview=overview,
        events=events
    )

@app.get([
    '/history',
    '/history/',
    '/<system_id>/history',
    '/<system_id>/history/'
])
def history_last_seen_page(system_id=None):
    overviews = [o for o in helpers.overview.find_all(system_id) if o.last_record is not None and not o.bus.is_test]
    return page('history/last_seen', system_id,
        title='Vehicle History',
        path='history',
        overviews=sorted(overviews, key=lambda o: o.bus)
    )

@app.get([
    '/history/first-seen',
    '/history/first-seen/',
    '/<system_id>/history/first-seen',
    '/<system_id>/history/first-seen/'
])
def history_first_seen_page(system_id=None):
    overviews = [o for o in helpers.overview.find_all(system_id) if o.first_record is not None and not o.bus.is_test]
    return page('history/first_seen', system_id,
        title='Vehicle History',
        path='history/first-seen',
        overviews=sorted(overviews, key=lambda o: (o.first_record.date, o.first_record.first_seen, o.bus), reverse=True)
    )

@app.get([
    '/history/transfers',
    '/history/transfers/',
    '/<system_id>/history/transfers',
    '/<system_id>/history/transfers/'
])
def history_transfers_page(system_id=None):
    return page('history/transfers', system_id,
        title='Vehicle History',
        path='history/transfers',
        transfers=helpers.transfer.find_all(system_id)
    )

@app.get([
    '/routes',
    '/routes/',
    '/<system_id>/routes',
    '/<system_id>/routes/'
])
def routes_list_page(system_id=None):
    return page('routes/list', system_id,
        title='Routes',
        path='routes',
        enable_refresh=False
    )

@app.get([
    '/routes/map',
    '/routes/map/',
    '/<system_id>/routes/map',
    '/<system_id>/routes/map/'
])
def routes_map_page(system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        routes = []
    else:
        routes = system.get_routes()
    return page('routes/map', system_id,
        title='Routes',
        path='routes/map',
        enable_refresh=False,
        include_maps=len(routes) > 0,
        full_map=len(routes) > 0,
        routes=routes
    )

@app.get([
    '/routes/<route_number>',
    '/routes/<route_number>/',
    '/<system_id>/routes/<route_number>',
    '/<system_id>/routes/<route_number>/'
])
def route_overview_page(route_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'routes/{route_number}'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id,
            route_number=route_number
        )
    trips = sorted(route.get_trips(date=Date.today()))
    return page('route/overview', system_id,
        title=str(route),
        include_maps=len(route.trips) > 0,
        route=route,
        trips=trips,
        recorded_today=helpers.record.find_recorded_today(system, trips),
        scheduled_today=helpers.record.find_scheduled_today(system, trips),
        positions=helpers.position.find_all(system_id, route_id=route.id)
    )

@app.get([
    '/routes/<route_number>/map',
    '/routes/<route_number>/map/',
    '/<system_id>/routes/<route_number>/map',
    '/<system_id>/routes/<route_number>/map/'
])
def route_map_page(route_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'routes/{route_number}/map'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id,
            route_number=route_number
        )
    return page('route/map', system_id,
        title=str(route),
        include_maps=len(route.trips) > 0,
        full_map=len(route.trips) > 0,
        route=route,
        positions=helpers.position.find_all(system_id, route_id=route.id)
    )

@app.get([
    '/routes/<route_number>/schedule',
    '/routes/<route_number>/schedule/',
    '/<system_id>/routes/<route_number>/schedule',
    '/<system_id>/routes/<route_number>/schedule/'
])
def route_schedule_page(route_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'routes/{route_number}/schedule'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id,
            route_number=route_number
        )
    return page('route/schedule', system_id,
        title=str(route),
        enable_refresh=False,
        route=route
    )

@app.get([
    '/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/',
    '/<system_id>/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/<system_id>/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/'
])
def route_schedule_date_page(route_number, date_string, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'routes/{route_number}/schedule'
        )
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id,
            route_number=route_number
        )
    date = Date.parse_db(date_string, None)
    return page('route/date', system_id,
        title=str(route),
        enable_refresh=False,
        route=route,
        date=date
    )

@app.get([
    '/blocks',
    '/blocks/',
    '/<system_id>/blocks',
    '/<system_id>/blocks/'
])
def blocks_page(system_id=None):
    return page('blocks/list', system_id,
        title='Blocks',
        enable_refresh=False,
        path='blocks'
    )

@app.get([
    '/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/',
    '/<system_id>/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/<system_id>/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/'
])
def blocks_schedule_date_page(date_string, system_id=None):
    date = Date.parse_db(date_string, None)
    return page('blocks/date', system_id,
        title='Blocks',
        enable_reload=False,
        path=f'blocks/schedule/{date_string}',
        date=date
    )

@app.get([
    '/blocks/<block_id>',
    '/blocks/<block_id>/',
    '/<system_id>/blocks/<block_id>',
    '/<system_id>/blocks/<block_id>/'
])
def block_overview_page(block_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'blocks/{block_id}'
        )
    block = system.get_block(block_id)
    if block is None:
        return error_page('block', system_id,
            block_id=block_id
        )
    return page('block/overview', system_id, block=block,
        title=f'Block {block.id}',
        include_maps=True,
        positions=helpers.position.find_all(system_id, block_id=block_id)
    )

@app.get([
    '/blocks/<block_id>/map',
    '/blocks/<block_id>/map/',
    '/<system_id>/blocks/<block_id>/map',
    '/<system_id>/blocks/<block_id>/map/'
])
def block_map_page(block_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'blocks/{block_id}/map'
        )
    block = system.get_block(block_id)
    if block is None:
        return error_page('block', system_id,
            block_id=block_id
        )
    return page('block/map', system_id, block=block,
        title=f'Block {block.id}',
        include_maps=True,
        full_map=True,
        positions=helpers.position.find_all(system_id, block_id=block_id)
    )

@app.get([
    '/blocks/<block_id>/history',
    '/blocks/<block_id>/history/',
    '/<system_id>/blocks/<block_id>/history',
    '/<system_id>/blocks/<block_id>/history/'
])
def block_history_page(block_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'blocks/{block_id}/history'
        )
    block = system.get_block(block_id)
    if block is None:
        return error_page('block', system_id, block_id=block_id)
    records = helpers.record.find_all(system_id=system_id, block_id=block_id)
    events = []
    if len(records) > 0:
        events.append(Event(records[0].date, 'Last Tracked'))
        events.append(Event(records[-1].date, 'First Tracked'))
    return page('block/history', system_id,
        title=f'Block {block.id}',
        block=block,
        records=records,
        events=events
    )

@app.get([
    '/trips/<trip_id>',
    '/trips/<trip_id>/',
    '/<system_id>/trips/<trip_id>',
    '/<system_id>/trips/<trip_id>/'
])
def trip_overview_page(trip_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'trips/{trip_id}'
        )
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('trip', system_id,
            trip_id=trip_id
        )
    return page('trip/overview', system_id,
        title=f'Trip {trip.id}',
        include_maps=True,
        trip=trip,
        positions=helpers.position.find_all(system_id, trip_id=trip_id)
    )

@app.get([
    '/trips/<trip_id>/map',
    '/trips/<trip_id>/map/',
    '/<system_id>/trips/<trip_id>/map',
    '/<system_id>/trips/<trip_id>/map/'
])
def trip_map_page(trip_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'trips/{trip_id}/map'
        )
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('trip', system_id,
            trip_id=trip_id
        )
    return page('trip/map', system_id,
        title=f'Trip {trip.id}',
        include_maps=True,
        full_map=True,
        trip=trip,
        positions=helpers.position.find_all(system_id, trip_id=trip_id)
    )

@app.get([
    '/trips/<trip_id>/history',
    '/trips/<trip_id>/history/',
    '/<system_id>/trips/<trip_id>/history',
    '/<system_id>/trips/<trip_id>/history/'
])
def trip_history_page(trip_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'trips/{trip_id}/history'
        )
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('trip', system_id, trip_id=trip_id)
    records = helpers.record.find_all(system_id=system_id, trip_id=trip_id)
    events = []
    if len(records) > 0:
        events.append(Event(records[0].date, 'Last Tracked'))
        events.append(Event(records[-1].date, 'First Tracked'))
    return page('trip/history', system_id,
        title=f'Trip {trip.id}',
        trip=trip,
        records=records,
        events=events
    )

@app.get([
    '/stops',
    '/stops/',
    '/<system_id>/stops',
    '/<system_id>/stops/'
])
def stops_page(system_id=None):
    path = 'stops'
    search = request.query.get('search')
    if search is not None:
        path += f'?search={search}'
    return page('stops', system_id,
        title='Stops',
        enable_refresh=False,
        path=path,
        search=search
    )

@app.get([
    '/stops/<stop_number>',
    '/stops/<stop_number>/',
    '/<system_id>/stops/<stop_number>',
    '/<system_id>/stops/<stop_number>/'
])
def stop_overview_page(stop_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'stops/{stop_number}'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id,
            stop_number=stop_number
        )
    departures = sorted(stop.get_departures(date=Date.today()))
    trips = [d.trip for d in departures]
    positions = helpers.position.find_all(system_id, trip_id={t.id for t in trips})
    return page('stop/overview', system_id,
        title=f'Stop {stop.number}',
        include_maps=True,
        stop=stop,
        departures=departures,
        recorded_today=helpers.record.find_recorded_today(system, trips),
        scheduled_today=helpers.record.find_scheduled_today(system, trips),
        positions={p.trip.id: p for p in positions}
    )

@app.get([
    '/stops/<stop_number>/map',
    '/stops/<stop_number>/map/',
    '/<system_id>/stops/<stop_number>/map',
    '/<system_id>/stops/<stop_number>/map/'
])
def stop_map_page(stop_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'stops/{stop_number}/map'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id,
            stop_number=stop_number
        )
    return page('stop/map', system_id,
        title=f'Stop {stop.number}',
        include_maps=True,
        full_map=True,
        stop=stop
    )

@app.get([
    '/stops/<stop_number>/schedule',
    '/stops/<stop_number>/schedule/',
    '/<system_id>/stops/<stop_number>/schedule',
    '/<system_id>/stops/<stop_number>/schedule/'
])
def stop_schedule_page(stop_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'stops/{stop_number}/schedule'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id,
            stop_number=stop_number
        )
    return page('stop/schedule', system_id,
        title=f'Stop {stop.number}',
        enable_refresh=False,
        stop=stop
    )

@app.get([
    '/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/',
    '/<system_id>/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/<system_id>/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/'
])
def stop_schedule_date_page(stop_number, date_string, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id,
            path=f'stops/{stop_number}/schedule'
        )
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id,
            stop_number=stop_number
        )
    date = Date.parse_db(date_string, None)
    return page('stop/date', system_id,
        title=f'Stop {stop.number}',
        enable_refresh=False,
        stop=stop,
        date=date
    )

@app.get([
    '/about',
    '/about/',
    '/<system_id>/about',
    '/<system_id>/about/'
])
def about_page(system_id=None):
    return page('about', system_id,
        title='About',
        enable_refresh=False,
        path='about'
    )

@app.get([
    '/themes',
    '/themes/',
    '/<system_id>/themes',
    '/<system_id>/themes/'
])
def themes_page(system_id=None):
    redirect(get_url(helpers.system.find(system_id), 'personalize'))

@app.get([
    '/personalize',
    '/personalize/',
    '/<system_id>/personalize',
    '/<system_id>/personalize/'
])
def themes_page(system_id=None):
    theme_id = request.query.get('theme')
    if theme_id is not None:
        set_cookie('theme', theme_id)
    time_format = request.query.get('time_format')
    if time_format is not None:
        set_cookie('time_format', time_format)
    themes = helpers.theme.find_all()
    return page('personalize', system_id,
        title='Personalize',
        enable_refresh=False,
        path='personalize',
        themes=themes
    )

@app.get([
    '/systems',
    '/systems/',
    '/<system_id>/systems',
    '/<system_id>/systems/'
])
def systems_page(system_id=None):
    return page('systems', system_id,
        title='Systems',
        enable_refresh=False,
        path=request.query.get('path', '')
    )

@app.get([
    '/admin',
    '/admin/',
    '/admin/<key>',
    '/admin/<key>/',
    '/<system_id>/admin',
    '/<system_id>/admin/',
    '/<system_id>/admin/<key>',
    '/<system_id>/admin/<key>/'
])
def admin_page(key=None, system_id=None):
    if admin_key is None or key == admin_key:
        if key is None:
            path = 'admin'
        else:
            path = f'admin/{key}'
        return page('admin', system_id,
            title='Administration',
            enable_refresh=False,
            path=path,
            key=key,
            disable_indexing=True
        )
    return page('home', system_id,
        title='Home',
        enable_refresh=False
    )

# =============================================================
# JSON (API endpoints)
# =============================================================

@app.get([
    '/api/map.json',
    '/<system_id>/api/map.json'
])
def system_api_map(system_id=None):
    system = helpers.system.find(system_id)
    time_format = request.get_cookie('time_format')
    if system is None:
        last_updated = realtime.get_last_updated(time_format)
    else:
        last_updated = system.get_last_updated(time_format)
    positions = sorted(helpers.position.find_all(system_id, has_location=True), key=lambda p: p.lat, reverse=True)
    return {
        'positions': [p.json for p in positions],
        'last_updated': last_updated
    }

@app.get([
    '/api/shape/<shape_id>.json',
    '/<system_id>/api/shape/<shape_id>.json'
])
def api_shape_id(shape_id, system_id=None):
    return {
        'points': [p.json for p in helpers.point.find_all(system_id, shape_id)]
    }

@app.post([
    '/api/search',
    '/api/search/',
    '/<system_id>/api/search',
    '/<system_id>/api/search/'
])
def api_search(system_id=None):
    query = request.forms.get('query', '')
    system = helpers.system.find(system_id)
    matches = []
    if query != '':
        if query.isnumeric() and (system is None or system.realtime_enabled):
            matches += helpers.order.find_matches(query, helpers.overview.find_bus_numbers(system_id))
        if system is not None:
            matches += system.search_routes(query)
            matches += system.search_stops(query)
    matches = sorted([m for m in matches if m.value > 0])
    return {
        'results': [m.get_json(system, get_url) for m in matches[0:10]],
        'count': len(matches)
    }

@app.post([
    '/api/admin/reload-adornments',
    '/api/admin/reload-adornments/',
    '/api/admin/<key>/reload-adornments',
    '/api/admin/<key>/reload-adornments/',
    '/<system_id>/api/admin/reload-adornments',
    '/<system_id>/api/admin/reload-adornments/',
    '/<system_id>/api/admin/<key>/reload-adornments',
    '/<system_id>/api/admin/<key>/reload-adornments/'
])
def api_admin_reload_adornments(key=None, system_id=None):
    if admin_key is None or key == admin_key:
        helpers.adornment.delete_all()
        helpers.adornment.load()
        return 'Success'
    return 'Access denied'

@app.post([
    '/api/admin/reload-orders',
    '/api/admin/reload-orders/',
    '/api/admin/<key>/reload-orders',
    '/api/admin/<key>/reload-orders/',
    '/<system_id>/api/admin/reload-orders',
    '/<system_id>/api/admin/reload-orders/',
    '/<system_id>/api/admin/<key>/reload-orders',
    '/<system_id>/api/admin/<key>/reload-orders/'
])
def api_admin_reload_orders(key=None, system_id=None):
    if admin_key is None or key == admin_key:
        helpers.model.delete_all()
        helpers.order.delete_all()
        helpers.model.load()
        helpers.order.load()
        return 'Success'
    return 'Access denied'

@app.post([
    '/api/admin/reload-systems',
    '/api/admin/reload-systems/',
    '/api/admin/<key>/reload-systems',
    '/api/admin/<key>/reload-systems/',
    '/<system_id>/api/admin/reload-systems',
    '/<system_id>/api/admin/reload-systems/',
    '/<system_id>/api/admin/<key>/reload-systems',
    '/<system_id>/api/admin/<key>/reload-systems/'
])
def api_admin_reload_systems(key=None, system_id=None):
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
                realtime.update(system)
            if not realtime.validate(system):
                system.validation_errors += 1
        if running:
            realtime.update_records()
            cron.start(cron_id)
        return 'Success'
    return 'Access denied'

@app.post([
    '/api/admin/reload-themes',
    '/api/admin/reload-themes/',
    '/api/admin/<key>/reload-themes',
    '/api/admin/<key>/reload-themes/',
    '/<system_id>/api/admin/reload-themes',
    '/<system_id>/api/admin/reload-themes/',
    '/<system_id>/api/admin/<key>/reload-themes',
    '/<system_id>/api/admin/<key>/reload-themes/'
])
def api_admin_reload_themes(key=None, system_id=None):
    if admin_key is None or key == admin_key:
        helpers.theme.delete_all()
        helpers.theme.load()
        return 'Success'
    return 'Access denied'

@app.post([
    '/api/admin/restart-cron',
    '/api/admin/restart-cron/',
    '/api/admin/<key>/restart-cron',
    '/api/admin/<key>/restart-cron/',
    '/<system_id>/api/admin/restart-cron',
    '/<system_id>/api/admin/restart-cron/',
    '/<system_id>/api/admin/<key>/restart-cron',
    '/<system_id>/api/admin/<key>/restart-cron/'
])
def api_admin_restart_cron(key=None, system_id=None):
    if admin_key is None or key == admin_key:
        cron.stop(cron_id)
        cron.start(cron_id)
        return 'Success'
    return 'Access denied'

@app.post([
    '/api/admin/backup-database',
    '/api/admin/backup-database/',
    '/api/admin/<key>/backup-database',
    '/api/admin/<key>/backup-database/',
    '/<system_id>/api/admin/backup-database',
    '/<system_id>/api/admin/backup-database/',
    '/<system_id>/api/admin/<key>/backup-database',
    '/<system_id>/api/admin/<key>/backup-database/'
])
def api_admin_backup_database(key=None, system_id=None):
    if admin_key is None or key == admin_key:
        database.backup()
        return 'Success'
    return 'Access denied'

@app.post([
    '/api/admin/reload-gtfs/<reload_system_id>',
    '/api/admin/reload-gtfs/<reload_system_id>/',
    '/api/admin/<key>/reload-gtfs/<reload_system_id>',
    '/api/admin/<key>/reload-gtfs/<reload_system_id>/',
    '/<system_id>/api/admin/reload-gtfs/<reload_system_id>',
    '/<system_id>/api/admin/reload-gtfs/<reload_system_id>/',
    '/<system_id>/api/admin/<key>/reload-gtfs/<reload_system_id>',
    '/<system_id>/api/admin/<key>/reload-gtfs/<reload_system_id>/'
])
def api_admin_reload_gtfs(reload_system_id, key=None, system_id=None):
    if admin_key is None or key == admin_key:
        system = helpers.system.find(reload_system_id)
        if system is None:
            return 'Invalid system'
        gtfs.load(system, True)
        realtime.update(system)
        if not realtime.validate(system):
            system.validation_errors += 1
        realtime.update_records()
        return 'Success'
    return 'Access denied'

@app.post([
    '/api/admin/reload-realtime/<reload_system_id>',
    '/api/admin/reload-realtime/<reload_system_id>/',
    '/api/admin/<key>/reload-realtime/<reload_system_id>',
    '/api/admin/<key>/reload-realtime/<reload_system_id>/',
    '/<system_id>/api/admin/reload-realtime/<reload_system_id>',
    '/<system_id>/api/admin/reload-realtime/<reload_system_id>/',
    '/<system_id>/api/admin/<key>/reload-realtime/<reload_system_id>',
    '/<system_id>/api/admin/<key>/reload-realtime/<reload_system_id>/'
])
def api_admin_reload_gtfs(reload_system_id, key=None, system_id=None):
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
