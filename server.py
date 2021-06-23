from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, static_file, template, request
import cherrypy as cp

from models.system import get_system, all_systems
import gtfs
import realtime
import history

mapbox_api_key = ''
no_system_domain = 'bctracker.ca/{0}'
system_domain = '{0}.bctracker.ca/{1}'

def start():
    global mapbox_api_key, no_system_domain, system_domain

    realtime.load_translations()
    history.load_last_seen()

    for system in all_systems():
        if gtfs.downloaded(system):
            gtfs.load(system)
        else:
            gtfs.update(system)
            realtime.update_routes(system)
        realtime.update(system)
        if not gtfs.validate(system):
            gtfs.update(system)
            realtime.update_routes(system)
    history.update(realtime.active_buses())

    cp.config.update('server.conf')
    mapbox_api_key = cp.config['mapbox_api_key']
    no_system_domain = cp.config['no_system_domain']
    system_domain = cp.config['system_domain']

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

def systems_template(name, **kwargs):
    return template(f'templates/{name}', systems=all_systems(), get_url=get_url, last_updated=realtime.last_updated_string(), **kwargs)

def systems_invalid_template(system_id):
    return systems_template('invalid_system', system_id=system_id)

def systems_error_template(system, error, message=None):
    return systems_template('error', system=system, error=error, message=message)

# =============================================================
# Web framework: assign routes - its all Server side rendering
# =============================================================
app = Bottle()

@app.route('/style/<name:path>')
def style(name):
    return system_style(None, name)

@app.route('/<system_id>/style/<name:path>')
def system_style(system_id, name):
    return static_file(name, root='./style')

@app.route('/img/<name:path>')
def img(name):
    return system_img(None, name)

@app.route('/<system_id>/img/<name:path>')
def system_img(system_id, name):
    return static_file(name, root='./img')

@app.route('/')
def index():
    return system_index(None)

@app.route('/<system_id>')
@app.route('/<system_id>/')
def system_index(system_id):
    return systems_template('home', system=get_system(system_id))

@app.route('/systems')
@app.route('/systems/')
def systems():
    return system_systems(None)

@app.route('/<system_id>/systems')
@app.route('/<system_id>/systems/')
def system_systems(system_id):
    path = request.query.get('path', '')
    return systems_template('systems', system=get_system(system_id), path=path)

@app.route('/routes')
@app.route('/routes/')
def routes():
    return system_routes(None)

@app.route('/<system_id>/routes')
@app.route('/<system_id>/routes/')
def system_routes(system_id):
    return systems_template('routes', system=get_system(system_id), path='routes')

@app.route('/routes/<number:int>')
@app.route('/routes/<number:int>/')
def routes_number(number):
    return system_routes_number(None, number)

@app.route('/<system_id>/routes/<number:int>')
@app.route('/<system_id>/routes/<number:int>/')
def system_routes_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    route = system.get_route(number=number)
    if route is None:
        return systems_error_template(system, f'Route {number} not found')
    return systems_template('route', system=system, route=route)

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
    return systems_template('history', system=system, last_seen=last_seen, path='history')

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
    return systems_template('map', system=system, buses=buses, path='map')

@app.route('/realtime')
@app.route('/realtime/')
def route_realtime():
    return system_realtime(None)

@app.route('/<system_id>/realtime')
@app.route('/<system_id>/realtime/')
def system_realtime(system_id):
    reload = request.query.get('reload', 'false')
    if reload == 'true':
        realtime.reset_positions()
        for system in all_systems():
            try:
                realtime.update(system)
                if not gtfs.validate(system):
                    gtfs.update(system)
                    realtime.update_routes(system)
            except Exception as e:
                print(f'Error: Failed to update realtime for {system}')
                print(f'Error message: {e}')
        history.update(realtime.active_buses())
    group = request.query.get('group', 'all')
    system = get_system(system_id)
    if system is None:
        buses = realtime.active_buses()
    else:
        buses = [b for b in realtime.active_buses() if b.position.system == system]
    return systems_template('realtime', system=system, group=group, buses=buses, path=f'realtime?group={group}')

@app.route('/bus/<number:int>')
@app.route('/bus/<number:int>/')
def bus_number(number):
    return system_bus_number(None, number)

@app.route('/<system_id>/bus/<number:int>')
@app.route('/<system_id>/bus/<number:int>/')
def system_bus_number(system_id, number):
    system = get_system(system_id)
    bus = realtime.get_bus(number=number)
    if bus is None:
        return systems_error_template(system, f'Bus {number} not found')
    return systems_template('bus', system=system, bus=bus, history=sorted(history.load_bus_history(number)))

@app.route('/blocks')
@app.route('/blocks/')
def blocks():
    return system_blocks(None)

@app.route('/<system_id>/blocks')
@app.route('/<system_id>/blocks/')
def system_blocks(system_id):
    return systems_template('blocks', system=get_system(system_id), path='blocks')

@app.route('/blocks/<block_id>')
@app.route('/blocks/<block_id>/')
def blocks_id(block_id):
    return system_blocks_id(None, block_id)

@app.route('/<system_id>/blocks/<block_id>')
@app.route('/<system_id>/blocks/<block_id>/')
def system_blocks_id(system_id, block_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    block = system.get_block(block_id)
    if block is None:
        return systems_error_template(system, f'Block {block_id} Not Found', 'This block may be from an older version of GTFS which is no longer valid')
    return systems_template('block', system=system, block=block)

@app.route('/trips/<trip_id>')
@app.route('/trips/<trip_id>/')
def trips_id(trip_id):
    return system_trips_id(None, trip_id)

@app.route('/<system_id>/trips/<trip_id>')
@app.route('/<system_id>/trips/<trip_id>/')
def system_trips_id(system_id, trip_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    trip = system.get_trip(trip_id)
    if trip is None:
        return systems_error_template(system, f'Trip {trip_id} Not Found', 'This trip may be from an older version of GTFS which is no longer valid')
    return systems_template('trip', system=system, trip=trip)

@app.route('/stops/<number:int>')
@app.route('/stops/<number:int>/')
def stops_number(number):
    return system_stops_number(None, number)

@app.route('/<system_id>/stops/<number:int>')
@app.route('/<system_id>/stops/<number:int>/')
def system_stops_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    stop = system.get_stop(number=number)
    if stop is None:
        return systems_error_template(system, f'Stop {number} Not Found')
    return systems_template('stop', system=system, stop=stop)

@app.route('/about')
@app.route('/about/')
def about():
    return system_about(None)

@app.route('/<system_id>/about')
@app.route('/<system_id>/about/')
def system_about(system_id):
    return systems_template('about', system=get_system(system_id), path='about')