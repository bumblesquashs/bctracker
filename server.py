from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, static_file, template, redirect, request, response, debug
import cherrypy as cp
import sys

from models.bus_model import load_models
from models.bus_order import load_orders
from models.system import load_systems, get_system, all_systems

import gtfs
import realtime
import history

# Increase the version to force CSS reload
VERSION = 0

app = Bottle()

mapbox_api_key = ''
no_system_domain = 'bctracker.ca/{0}'
system_domain = '{0}.bctracker.ca/{1}'
cookie_domain = None

def start():
    global mapbox_api_key, no_system_domain, system_domain, cookie_domain
    
    force_gtfs_redownload = False
    if len(sys.argv):
        arg_str = ''.join(sys.argv[1:])
        if 'r' in arg_str:
            print('Forcing GTFS redownload')
            force_gtfs_redownload = True
        if 'd' in arg_str:
            print('Starting bottle in DEBUG mode')
            debug(True)
    
    load_models()
    load_orders()
    load_systems()
    
    realtime.load_translations()
    history.load_last_seen()
    
    for system in all_systems():
        if not gtfs.downloaded(system) or force_gtfs_redownload:
            gtfs.update(system)
        else:
            gtfs.load(system)
        realtime.update(system)
        if not gtfs.validate(system):
            gtfs.update(system)
        elif not realtime.validate(system):
            system.realtime_validation_error_count += 1
    history.update(realtime.active_buses())
    
    cp.config.update('server.conf')
    mapbox_api_key = cp.config['mapbox_api_key']
    no_system_domain = cp.config['no_system_domain']
    system_domain = cp.config['system_domain']
    cookie_domain = cp.config.get('cookie_domain')
    
    handler = TimedRotatingFileHandler(filename='logs/access_log.log', when='d', interval=7)
    log = WSGILogger(app, [handler], ApacheFormatter())
    
    cp.tree.graft(log, '/')
    cp.server.start()

def stop():
    cp.server.stop()

def get_url(system, path=''):
    if system is None:
        return no_system_domain.format(path).rstrip('/')
    if isinstance(system, str):
        return system_domain.format(system, path).rstrip('/')
    return system_domain.format(system.id, path).rstrip('/')

def systems_template(name, system_id, theme=None, **kwargs):
    return template(f'pages/{name}',
        mapbox_api_key=mapbox_api_key,
        systems=[s for s in all_systems() if s.visible],
        system_id=system_id,
        system=get_system(system_id),
        get_url=get_url,
        last_updated=realtime.last_updated_string(),
        theme=theme or request.get_cookie('theme'),
        version=VERSION,
        no_system_domain=no_system_domain,
        system_domain=system_domain,
        **kwargs
    )

def systems_error_template(name, system_id, **kwargs):
    return systems_template(f'errors/{name}_error', system_id, **kwargs)

# =============================================================
# CSS (Static Files)
# =============================================================

@app.route('/style/<name:path>')
def style(name):
    return system_style(None, name)

@app.route('/<system_id>/style/<name:path>')
def system_style(system_id, name):
    return static_file(name, root='./style')

# =============================================================
# Images (Static Files)
# =============================================================

@app.route('/img/<name:path>')
def img(name):
    return system_img(None, name)

@app.route('/<system_id>/img/<name:path>')
def system_img(system_id, name):
    return static_file(name, root='./img')

# =============================================================
# HTML (Templates)
# =============================================================

@app.route('/')
def index():
    return system_index(None)

@app.route('/<system_id>')
@app.route('/<system_id>/')
def system_index(system_id):
    theme = request.query.get('theme')
    if theme is not None:
        max_age = 60*60*24*365*10
        if cookie_domain is None:
            response.set_cookie('theme', theme, max_age=max_age)
        else:
            response.set_cookie('theme', theme, max_age=max_age, domain=cookie_domain)
    return systems_template('home', system_id, theme)

@app.route('/news')
@app.route('/news/')
def news():
    return system_news(None)

@app.route('/<system_id>/news')
@app.route('/<system_id>/news/')
def system_news(system_id):
    return systems_template('news', system_id, path='news')

@app.route('/map')
@app.route('/map/')
def map():
    return system_map(None)

@app.route('/<system_id>/map')
@app.route('/<system_id>/map/')
def system_map(system_id):
    system = get_system(system_id)
    if system is None:
        buses = realtime.active_buses()
    else:
        buses = [b for b in realtime.active_buses() if b.position.system == system]
    return systems_template('map', system_id, buses=buses, path='map')

@app.route('/realtime')
@app.route('/realtime/')
def route_realtime():
    return system_realtime(None)

@app.route('/<system_id>/realtime')
@app.route('/<system_id>/realtime/')
def system_realtime(system_id):
    group = request.query.get('group', 'all')
    system = get_system(system_id)
    if system is None:
        buses = realtime.active_buses()
    else:
        buses = [b for b in realtime.active_buses() if b.position.system == system]
    return systems_template('realtime', system_id, group=group, buses=buses, path=f'realtime?group={group}')

@app.route('/bus/<number:int>')
@app.route('/bus/<number:int>/')
def bus_number(number):
    return system_bus_number(None, number)

@app.route('/<system_id>/bus/<number:int>')
@app.route('/<system_id>/bus/<number:int>/')
def system_bus_number(system_id, number):
    bus = realtime.get_bus(number=number)
    if bus is None:
        return systems_error_template('bus', system_id, number=number)
    return systems_template('bus', system_id, bus=bus, history=sorted(history.load_bus_history(number)))

@app.route('/bus/<number:int>/history')
@app.route('/bus/<number:int>/history/')
def bus_number_history(number):
    return system_bus_number_history(None, number)

@app.route('/<system_id>/bus/<number:int>/history')
@app.route('/<system_id>/bus/<number:int>/history/')
def system_bus_number_history(system_id, number):
    bus = realtime.get_bus(number=number)
    if bus is None:
        return systems_error_template('bus', system_id, number=number)
    return systems_template('bus_history', system_id, bus=bus, history=sorted(history.load_bus_history(number)))

@app.route('/history')
@app.route('/history/')
def route_history():
    return system_history(None)

@app.route('/<system_id>/history')
@app.route('/<system_id>/history/')
def system_history(system_id):
    system = get_system(system_id)
    if system is None:
        last_seen = history.all_last_seen()
    else:
        last_seen = [h for h in history.all_last_seen() if h.system == system]
    return systems_template('history', system_id, last_seen=last_seen, path='history')

@app.route('/routes')
@app.route('/routes/')
def routes():
    return system_routes(None)

@app.route('/<system_id>/routes')
@app.route('/<system_id>/routes/')
def system_routes(system_id):
    return systems_template('routes', system_id, path='routes')

@app.route('/routes/<number>')
@app.route('/routes/<number>/')
def routes_number(number):
    return system_routes_number(None, number)

@app.route('/<system_id>/routes/<number>')
@app.route('/<system_id>/routes/<number>/')
def system_routes_number(system_id, number):
    if (system_id == 'chilliwack' or system_id == 'cfv') and number == '66':
        redirect(get_url('fvx', 'routes/66'))
    system = get_system(system_id)
    if system is None:
        return systems_error_template('system', system_id, path=f'routes/{number}')
    route = system.get_route(number=number)
    if route is None:
        return systems_error_template('route', system_id, number=number)
    return systems_template('route', system_id, route=route)

@app.route('/blocks')
@app.route('/blocks/')
def blocks():
    return system_blocks(None)

@app.route('/<system_id>/blocks')
@app.route('/<system_id>/blocks/')
def system_blocks(system_id):
    return systems_template('blocks', system_id, path='blocks')

@app.route('/blocks/<block_id>')
@app.route('/blocks/<block_id>/')
def blocks_id(block_id):
    return system_blocks_id(None, block_id)

@app.route('/<system_id>/blocks/<block_id>')
@app.route('/<system_id>/blocks/<block_id>/')
def system_blocks_id(system_id, block_id):
    system = get_system(system_id)
    if system is None:
        return systems_error_template('system', system_id, path=f'blocks/{block_id}')
    block = system.get_block(block_id)
    if block is None:
        return systems_error_template('block', system_id, block_id=block_id)
    return systems_template('block', system_id, block=block)

@app.route('/trips/<trip_id>')
@app.route('/trips/<trip_id>/')
def trips_id(trip_id):
    return system_trips_id(None, trip_id)

@app.route('/<system_id>/trips/<trip_id>')
@app.route('/<system_id>/trips/<trip_id>/')
def system_trips_id(system_id, trip_id):
    system = get_system(system_id)
    if system is None:
        return systems_error_template('system', system_id, path=f'trips/{trip_id}')
    trip = system.get_trip(trip_id)
    if trip is None:
        return systems_error_template('trip', system_id, trip_id=trip_id)
    return systems_template('trip', system_id, trip=trip)

@app.route('/stops')
@app.route('/stops/')
def stops():
    return system_stops(None)

@app.route('/<system_id>/stops')
@app.route('/<system_id>/stops/')
def system_stops(system_id):
    path = 'stops'
    search = request.query.get('search')
    if search is not None:
        path += f'?search={search}'
    return systems_template('stops', system_id, search=search, path=path)

@app.route('/stops/<number:int>')
@app.route('/stops/<number:int>/')
def stops_number(number):
    return system_stops_number(None, number)

@app.route('/<system_id>/stops/<number:int>')
@app.route('/<system_id>/stops/<number:int>/')
def system_stops_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return systems_error_template('system', system_id, path=f'stops/{number}')
    stop = system.get_stop(number=number)
    if stop is None:
        return systems_error_template('stop', system_id, number=number)
    return systems_template('stop', system_id, stop=stop)

@app.route('/about')
@app.route('/about/')
def about():
    return system_about(None)

@app.route('/<system_id>/about')
@app.route('/<system_id>/about/')
def system_about(system_id):
    return systems_template('about', system_id, path='about')

@app.route('/systems')
@app.route('/systems/')
def systems():
    return system_systems(None)

@app.route('/<system_id>/systems')
@app.route('/<system_id>/systems/')
def system_systems(system_id):
    path = request.query.get('path', '')
    return systems_template('systems', system_id, path=path)

# =============================================================
# JSON (API endpoints)
# =============================================================

@app.route('/api/map.json')
def api_map():
    return system_api_map(None)

@app.route('/<system_id>/api/map.json')
def system_api_map(system_id):
    system = get_system(system_id)
    if system is None:
        buses = realtime.active_buses()
    else:
        buses = [b for b in realtime.active_buses() if b.position.system == system]
    return {
        'buses': [b.json_data for b in buses if b.position.has_location],
        'last_updated': realtime.last_updated_string()
    }

@app.route('/<system_id>/api/shape/<shape_id>.json')
def system_api_shape_id(system_id, shape_id):
    system = get_system(system_id)
    if system is None:
        return {}
    shape = system.get_shape(shape_id)
    if shape is None:
        return {}
    return {
        'points': [p.json_data for p in shape.points]
    }
