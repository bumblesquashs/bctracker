
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import Bottle, static_file, template, request
import cherrypy as cp

from models.system import get_system, all_systems
import gtfs

DEFAULT_SYSTEM_ID = 'victoria'

mapbox_api_key = ''

def start():
    global mapbox_api_key

    for system in all_systems():
        if gtfs.downloaded(system):
            system.load_gtfs()
        else:
            system.update_gtfs()
        system.update_realtime()
        if not system.validate_gtfs():
            system.update_gtfs()

    cp.config.update('server.conf')
    mapbox_api_key = cp.config['mapbox_api_key']

    handler = TimedRotatingFileHandler(filename='logs/access_log.log', when='d', interval=7)
    log = WSGILogger(app, [handler], ApacheFormatter())

    cp.tree.graft(log, '/')
    cp.server.start()

def stop():
    cp.server.stop()

def systems_template(name, **kwargs):
    return template(f'templates/{name}', systems=all_systems(), **kwargs)

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
    return system_style(DEFAULT_SYSTEM_ID, name)

@app.route('/<system_id>/style/<name:path>')
def system_style(system_id, name):
    return static_file(name, root='./style')

@app.route('/img/<name:path>')
def img(name):
    return static_file(name, root='./img')

@app.route('/<system_id>/img/<name:path>')
def system_img(system_id, name):
    return static_file(name, root='./img')

@app.route('/')
def index():
    return system_index(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>')
def system_index(system_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    return systems_template('home', system=system)

@app.route('/routes')
def routes():
    return system_routes(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>/routes')
def system_routes(system_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    return systems_template('routes', system=system)

@app.route('/routes/<number>')
def routes_number(number):
    return system_routes_number(DEFAULT_SYSTEM_ID, number)

@app.route('/<system_id>/routes/<number>')
def system_routes_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    route = system.get_route(number=number)
    if route is None:
        return systems_error_template(system, f'Route {number} not found')
    return systems_template('route', system=system, route=route)

@app.route('/history')
def history():
    return system_history(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>/history')
def system_history(system_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    return systems_template('history', system=system)

@app.route('/realtime')
def realtime():
    return system_realtime(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>/realtime')
def system_realtime(system_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    group = request.query.get('group', 'all')
    return systems_template('realtime', system=system, group=group)

@app.route('/bus/<number>')
def bus_number(number):
    return system_bus_number(DEFAULT_SYSTEM_ID, number)

@app.route('/<system_id>/bus/<number>')
def system_bus_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    bus = system.get_bus(number=number)
    if bus is None:
        return systems_error_template(system, f'Bus {number} not found')
    return systems_template('bus', system=system, bus=bus)

@app.route('/blocks')
def blocks():
    return system_blocks(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>/blocks')
def system_blocks(system_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    return systems_template('blocks', system=system)

@app.route('/blocks/<block_id>')
def blocks_id(block_id):
    return system_blocks_id(DEFAULT_SYSTEM_ID, block_id)

@app.route('/<system_id>/blocks/<block_id>')
def system_blocks_id(system_id, block_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    block = system.get_block(block_id)
    if block is None:
        return systems_error_template(system, f'Block {block_id} Not Found', 'This block may be from an older version of GTFS which is no longer valid')
    return systems_template('block', system=system, block=block)

@app.route('/trips/<trip_id>')
def trips_id(trip_id):
    return system_trips_id(DEFAULT_SYSTEM_ID, trip_id)

@app.route('/<system_id>/trips/<trip_id>')
def system_trips_id(system_id, trip_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    trip = system.get_trip(trip_id)
    if trip is None:
        return systems_error_template(system, f'Trip {trip_id} Not Found', 'This trip may be from an older version of GTFS which is no longer valid')
    return systems_template('trip', system=system, trip=trip)

@app.route('/stops/<number>')
def stops_number(number):
    return system_stops_number(DEFAULT_SYSTEM_ID, number)

@app.route('/<system_id>/stops/<number>')
def system_stops_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    stop = system.get_stop(number=number)
    if stop is None:
        return systems_error_template(system, f'Stop {number} Not Found')
    return systems_template('stop', system=system, stop=stop)

@app.route('/about')
def about():
    return system_about(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>/about')
def system_about(system_id):
    system = get_system(system_id)
    if system is None:
        return systems_invalid_template(system_id)
    return systems_template('about', system=system)