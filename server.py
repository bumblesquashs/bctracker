
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, static_file, template, request, response, debug, redirect
import cherrypy as cp

import helpers.model
import helpers.order
import helpers.overview
import helpers.record
import helpers.region
import helpers.system
import helpers.theme
import helpers.transfer

from models.bus import Bus
from models.date import Date

import cron
import database
import gtfs
import realtime

# Increase the version to force CSS reload
VERSION = 15

app = Bottle()

cron_id = 'bctracker-muncher'
mapbox_api_key = ''
no_system_domain = 'https://bctracker.ca/{0}'
system_domain = 'https://{0}.bctracker.ca/{1}'
system_domain_path = 'https://bctracker.ca/{0}/{1}'
cookie_domain = None
admin_key = None

def start(args):
    '''Loads all required data and launches the server'''
    global cron_id, mapbox_api_key, no_system_domain, system_domain, system_domain_path, cookie_domain, admin_key
    
    database.connect()
    
    if args.debug:
        print('Starting bottle in DEBUG mode')
        debug(True)
    if args.reload:
        print('Forcing GTFS redownload')
    
    helpers.model.load()
    helpers.order.load()
    helpers.region.load()
    helpers.system.load()
    helpers.theme.load()
    
    for system in helpers.system.find_all():
        gtfs.load(system, args.reload)
        if not gtfs.validate(system):
            gtfs.load(system, True)
        realtime.update(system)
        if not realtime.validate(system):
            system.validation_errors += 1
    realtime.update_records()
    
    cron.setup()
    cron.start(cron_id)
    
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

def stop():
    '''Terminates the server'''
    cron.stop(cron_id)
    database.disconnect()
    cp.server.stop()

def get_url(system, path=''):
    '''Returns a URL formatted based on the given system and path'''
    if system is None:
        return no_system_domain.format(path).rstrip('/')
    if isinstance(system, str):
        return system_domain.format(system, path).rstrip('/')
    return system_domain.format(system.id, path).rstrip('/')

def page(name, system_id, path='', **kwargs):
    '''Returns an HTML page with the given name and details'''
    theme_id = request.query.get('theme') or request.get_cookie('theme')
    time_format = request.query.get('time_format') or request.get_cookie('time_format')
    system = helpers.system.find(system_id)
    if system is None:
        last_updated = realtime.get_last_updated(time_format)
    else:
        last_updated = system.get_last_updated(time_format)
    return template(f'pages/{name}',
        version=VERSION,
        path=path,
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
        show_speed=request.get_cookie('speed') == '1994',
        **kwargs
    )

def error_page(name, system_id, path='', **kwargs):
    '''Returns an error page with the given name and details'''
    return page(f'errors/{name}_error', system_id, path, **kwargs)

def set_cookie(key, value):
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
    return page('home', system_id)

@app.get([
    '/news',
    '/news/',
    '/<system_id>/news',
    '/<system_id>/news/'
])
def news_page(system_id=None):
    return page('news', system_id, path='news')

@app.get([
    '/map',
    '/map/',
    '/<system_id>/map',
    '/<system_id>/map/'
])
def map_page(system_id=None):
    positions = sorted([p for p in realtime.get_positions(system_id) if p.has_location], key=lambda p: p.lat, reverse=True)
    return page('map', system_id, path='map', positions=positions)

@app.get([
    '/realtime',
    '/realtime/',
    '/<system_id>/realtime',
    '/<system_id>/realtime/'
])
def realtime_all_page(system_id=None):
    positions = realtime.get_positions(system_id)
    return page('realtime/all', system_id, path='realtime', positions=positions)

@app.get([
    '/realtime/routes',
    '/realtime/routes/',
    '/<system_id>/realtime/routes',
    '/<system_id>/realtime/routes/'
])
def realtime_routes_page(system_id=None):
    positions = realtime.get_positions(system_id)
    return page('realtime/routes', system_id, path='realtime/routes', positions=positions)

@app.get([
    '/realtime/models',
    '/realtime/models/',
    '/<system_id>/realtime/models',
    '/<system_id>/realtime/models/'
])
def realtime_models_page(system_id=None):
    positions = realtime.get_positions(system_id)
    return page('realtime/models', system_id, path='realtime/models', positions=positions)

@app.get([
    '/realtime/speed',
    '/realtime/speed/',
    '/<system_id>/realtime/speed',
    '/<system_id>/realtime/speed/'
])
def realtime_speed_page(system_id=None):
    set_cookie('speed', '1994')
    positions = realtime.get_positions(system_id)
    return page('realtime/speed', system_id, path='realtime/speed', positions=positions)

@app.get([
    '/fleet',
    '/fleet/',
    '/<system_id>/fleet',
    '/<system_id>/fleet/'
])
def fleet_page(system_id=None):
    orders = [o for o in sorted(helpers.order.find_all(), key=lambda o: o.low) if not o.is_test]
    overviews = helpers.overview.find_all()
    return page('fleet', system_id, path='fleet', orders=orders, overviews={o.bus.number: o for o in overviews})

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
        return error_page('bus', system_id, bus_number=bus_number)
    position = realtime.get_position(bus_number)
    records = helpers.record.find_all(bus_number=bus_number, limit=20)
    return page('bus/overview', system_id, bus=bus, position=position, records=records)

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
        return error_page('bus', system_id, bus_number=bus_number)
    position = realtime.get_position(bus_number)
    return page('bus/map', system_id, bus=bus, position=position)

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
        return error_page('bus', system_id, bus_number=bus_number)
    records = helpers.record.find_all(bus_number=bus_number)
    return page('bus/history', system_id, bus=bus, records=records)

@app.get([
    '/history',
    '/history/',
    '/<system_id>/history',
    '/<system_id>/history/'
])
def history_last_seen_page(system_id=None):
    overviews = sorted([o for o in helpers.overview.find_all(system_id) if o.last_record is not None and not o.bus.is_test], key=lambda o: o.bus)
    return page('history/last_seen', system_id, path='history', overviews=overviews)

@app.get([
    '/history/first-seen',
    '/history/first-seen/',
    '/<system_id>/history/first-seen',
    '/<system_id>/history/first-seen/'
])
def history_first_seen_page(system_id=None):
    overviews = sorted([o for o in helpers.overview.find_all(system_id) if o.first_record is not None and not o.bus.is_test], key=lambda o: (o.first_record.date, o.first_record.first_seen, o.bus), reverse=True)
    return page('history/first_seen', system_id, path='history/first-seen', overviews=overviews)

@app.get([
    '/history/transfers',
    '/history/transfers/',
    '/<system_id>/history/transfers',
    '/<system_id>/history/transfers/'
])
def history_transfers_page(system_id=None):
    transfers = helpers.transfer.find_all(system_id)
    return page('history/transfers', system_id, path='history/transfers', transfers=transfers)

@app.get([
    '/routes',
    '/routes/',
    '/<system_id>/routes',
    '/<system_id>/routes/'
])
def routes_list_page(system_id=None):
    return page('routes/list', system_id, path='routes')

@app.get([
    '/routes/map',
    '/routes/map/',
    '/<system_id>/routes/map',
    '/<system_id>/routes/map/'
])
def routes_map_page(system_id=None):
    return page('routes/map', system_id, path='routes/map')

@app.get([
    '/routes/<route_number>',
    '/routes/<route_number>/',
    '/<system_id>/routes/<route_number>',
    '/<system_id>/routes/<route_number>/'
])
def route_overview_page(route_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'routes/{route_number}')
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id, route_number=route_number)
    positions = [p for p in realtime.get_positions(system_id) if p.trip is not None and p.trip.route_id == route.id]
    trips = sorted([t for t in route.trips if t.service.is_today])
    recorded_today = helpers.record.find_recorded_today(system, trips)
    scheduled_today = helpers.record.find_scheduled_today(system, trips)
    return page('route/overview', system_id, route=route, positions=positions, trips=trips, recorded_today=recorded_today, scheduled_today=scheduled_today)

@app.get([
    '/routes/<route_number>/map',
    '/routes/<route_number>/map/',
    '/<system_id>/routes/<route_number>/map',
    '/<system_id>/routes/<route_number>/map/'
])
def route_map_page(route_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'routes/{route_number}/map')
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id, route_number=route_number)
    positions = [p for p in realtime.get_positions(system_id) if p.trip is not None and p.trip.route_id == route.id]
    return page('route/map', system_id, route=route, positions=positions)

@app.get([
    '/routes/<route_number>/schedule',
    '/routes/<route_number>/schedule/',
    '/<system_id>/routes/<route_number>/schedule',
    '/<system_id>/routes/<route_number>/schedule/'
])
def route_schedule_page(route_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'routes/{route_number}/schedule')
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id, route_number=route_number)
    return page('route/schedule', system_id, route=route)

@app.get([
    '/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/',
    '/<system_id>/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/<system_id>/routes/<route_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/'
])
def route_schedule_date_page(route_number, date_string, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'routes/{route_number}/schedule')
    route = system.get_route(number=route_number)
    if route is None:
        return error_page('route', system_id, route_number=route_number)
    date = Date.parse_db(date_string, None)
    return page('route/date', system_id, route=route, date=date)

@app.get([
    '/blocks',
    '/blocks/',
    '/<system_id>/blocks',
    '/<system_id>/blocks/'
])
def blocks_page(system_id=None):
    return page('blocks/list', system_id, path='blocks')

@app.get([
    '/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/',
    '/<system_id>/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/<system_id>/blocks/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/'
])
def blocks_schedule_date_page(date_string, system_id=None):
    date = Date.parse_db(date_string, None)
    return page('blocks/date', system_id, path=f'blocks/schedule/{date_string}', date=date)

@app.get([
    '/blocks/<block_id>',
    '/blocks/<block_id>/',
    '/<system_id>/blocks/<block_id>',
    '/<system_id>/blocks/<block_id>/'
])
def block_overview_page(block_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'blocks/{block_id}')
    block = system.get_block(block_id)
    if block is None:
        return error_page('block', system_id, block_id=block_id)
    positions = [p for p in realtime.get_positions(system_id) if p.trip is not None and p.trip.block_id == block_id]
    return page('block/overview', system_id, block=block, positions=positions)

@app.get([
    '/blocks/<block_id>/map',
    '/blocks/<block_id>/map/',
    '/<system_id>/blocks/<block_id>/map',
    '/<system_id>/blocks/<block_id>/map/'
])
def block_map_page(block_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'blocks/{block_id}/map')
    block = system.get_block(block_id)
    if block is None:
        return error_page('block', system_id, block_id=block_id)
    positions = [p for p in realtime.get_positions(system_id) if p.trip is not None and p.trip.block_id == block_id]
    return page('block/map', system_id, block=block, positions=positions)

@app.get([
    '/blocks/<block_id>/history',
    '/blocks/<block_id>/history/',
    '/<system_id>/blocks/<block_id>/history',
    '/<system_id>/blocks/<block_id>/history/'
])
def block_history_page(block_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'blocks/{block_id}/history')
    block = system.get_block(block_id)
    if block is None:
        return error_page('block', system_id, block_id=block_id)
    records = helpers.record.find_all(system_id=system_id, block_id=block_id)
    return page('block/history', system_id, block=block, records=records)

@app.get([
    '/trips/<trip_id>',
    '/trips/<trip_id>/',
    '/<system_id>/trips/<trip_id>',
    '/<system_id>/trips/<trip_id>/'
])
def trip_overview_page(trip_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'trips/{trip_id}')
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('trip', system_id, trip_id=trip_id)
    positions = [p for p in realtime.get_positions(system_id) if p.trip_id == trip_id]
    return page('trip/overview', system_id, trip=trip, positions=positions)

@app.get([
    '/trips/<trip_id>/map',
    '/trips/<trip_id>/map/',
    '/<system_id>/trips/<trip_id>/map',
    '/<system_id>/trips/<trip_id>/map/'
])
def trip_map_page(trip_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'trips/{trip_id}/map')
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('trip', system_id, trip_id=trip_id)
    positions = [p for p in realtime.get_positions(system_id) if p.trip_id == trip_id]
    return page('trip/map', system_id, trip=trip, positions=positions)

@app.get([
    '/trips/<trip_id>/history',
    '/trips/<trip_id>/history/',
    '/<system_id>/trips/<trip_id>/history',
    '/<system_id>/trips/<trip_id>/history/'
])
def trip_history_page(trip_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'trips/{trip_id}/history')
    trip = system.get_trip(trip_id)
    if trip is None:
        return error_page('trip', system_id, trip_id=trip_id)
    records = helpers.record.find_all(system_id=system_id, trip_id=trip_id)
    return page('trip/history', system_id, trip=trip, records=records)

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
    return page('stops', system_id, search=search, path=path)

@app.get([
    '/stops/<stop_number>',
    '/stops/<stop_number>/',
    '/<system_id>/stops/<stop_number>',
    '/<system_id>/stops/<stop_number>/'
])
def stop_overview_page(stop_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'stops/{stop_number}')
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id, stop_number=stop_number)
    departures = sorted([d for d in stop.departures if d.trip.service.is_today])
    trips = [d.trip for d in departures]
    positions = {p.trip.id:p for p in realtime.get_positions(system_id) if p.trip is not None and p.trip in trips}
    recorded_today = helpers.record.find_recorded_today(system, trips)
    scheduled_today = helpers.record.find_scheduled_today(system, trips)
    return page('stop/overview', system_id, stop=stop, departures=departures, positions=positions, recorded_today=recorded_today, scheduled_today=scheduled_today)

@app.get([
    '/stops/<stop_number>/map',
    '/stops/<stop_number>/map/',
    '/<system_id>/stops/<stop_number>/map',
    '/<system_id>/stops/<stop_number>/map/'
])
def stop_map_page(stop_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'stops/{stop_number}/map')
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id, stop_number=stop_number)
    return page('stop/map', system_id, stop=stop)

@app.get([
    '/stops/<stop_number>/schedule',
    '/stops/<stop_number>/schedule/',
    '/<system_id>/stops/<stop_number>/schedule',
    '/<system_id>/stops/<stop_number>/schedule/'
])
def stop_schedule_page(stop_number, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'stops/{stop_number}/schedule')
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id, stop_number=stop_number)
    return page('stop/schedule', system_id, stop=stop)

@app.get([
    '/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/',
    '/<system_id>/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>',
    '/<system_id>/stops/<stop_number>/schedule/<date_string:re:\\d{4}-\\d{2}-\\d{2}>/'
])
def stop_schedule_date_page(stop_number, date_string, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return error_page('system', system_id, path=f'stops/{stop_number}/schedule')
    stop = system.get_stop(number=stop_number)
    if stop is None:
        return error_page('stop', system_id, stop_number=stop_number)
    date = Date.parse_db(date_string, None)
    return page('stop/date', system_id, stop=stop, date=date)

@app.get([
    '/about',
    '/about/',
    '/<system_id>/about',
    '/<system_id>/about/'
])
def about_page(system_id=None):
    return page('about', system_id, path='about')

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
    return page('personalize', system_id, path='personalize', themes=themes)

@app.get([
    '/systems',
    '/systems/',
    '/<system_id>/systems',
    '/<system_id>/systems/'
])
def systems_page(system_id=None):
    return page('systems', system_id, path=request.query.get('path', ''))

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
        return page('admin', system_id, path=path, key=key)
    return page('home', system_id)

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
    positions = sorted([p for p in realtime.get_positions(system_id) if p.has_location], key=lambda p: p.lat, reverse=True)
    return {
        'positions': [p.json for p in positions],
        'last_updated': last_updated
    }

@app.get([
    '/api/shape/<shape_id>.json',
    '/<system_id>/api/shape/<shape_id>.json'
])
def api_shape_id(shape_id, system_id=None):
    system = helpers.system.find(system_id)
    if system is None:
        return {}
    shape = system.get_shape(shape_id)
    if shape is None:
        return {}
    return {
        'points': [p.json for p in shape.points]
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
