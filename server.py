
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from requestlogger import WSGILogger, ApacheFormatter
from bottle import template, Bottle, static_file
import cherrypy as cp

from models.system import get_system, all_systems
import gtfs

DEFAULT_SYSTEM_ID = 'victoria'

mapbox_api_key = ''

def start():
    global mapbox_api_key

    for system in all_systems():
        # gtfs.update(system.system_id)
        system.reload()

    cp.config.update('server.conf')
    mapbox_api_key = cp.config['mapbox_api_key']

    cp.tree.graft(make_access_log(app, 'logs/access_log.log'), '/')
    cp.server.start()

def make_access_log(app, filepath, when='d', interval=7, **kwargs):
    if filepath is None:
        handlers = [StreamHandler()]
    else:
        handlers = [TimedRotatingFileHandler(filepath, when, interval, **kwargs)]
    return WSGILogger(app, handlers, ApacheFormatter())

def stop():
    cp.server.stop()

# =============================================================
# Web framework: assign routes - its all Server side rendering
# =============================================================
app = Bottle()

@app.route('/style/<name:path>')
def style(name):
    return static_file(name, root='./style')

@app.route('/img/<name:path>')
def style(name):
    return static_file(name, root='./img')

@app.route('/')
def index():
    return system_index(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>')
def system_index(system_id):
    system = get_system(system_id)
    if system is None:
        return template('templates/invalid_system', systems=all_systems(), system_id=system_id)
    return template('templates/home', systems=all_systems(), system=system)

@app.route('/routes')
def routes():
    return system_routes(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>/routes')
def system_routes(system_id):
    system = get_system(system_id)
    if system is None:
        return template('templates/invalid_system', systems=all_systems(), system_id=system_id)
    return template('templates/routes', systems=all_systems(), system=system)

@app.route('/routes/<number:int>')
def routes_number(number):
    return system_routes_number(DEFAULT_SYSTEM_ID, number)

@app.route('/<system_id>/routes/<number:int>')
def system_routes_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return template('templates/invalid_system', systems=all_systems(), system_id=system_id)
    route = system.get_route(number=number)
    if route is None:
        return template('templates/error', systems=all_systems(), system=system, error=f'Route {number} not found')
    return template('templates/route', systems=all_systems(), system=system, route=route)


# @app.route('/history')
# def history():
#     return template('history')

# @app.route('/realtime')
# @app.route('/realtime/all')
# def realtime():
#     if 'rt' in request.query:
#         rt.download_lastest_files()
#         valid = rt.load_realtime()
#         if((not valid) and start.RELOAD_ENABLED):
#             start.download_and_restart()
#         hist.update_last_seen()
#     group = request.query.get('group', 'all')
#     rtbuslist = []
#     for busid in rt.rtvehicle_dict:
#         bus = rt.rtvehicle_dict[busid]
#         try:
            # if we know the real time translation, add it here
#             fleet_num = rt.id2fleetnum_dict[busid]
#             bus.fleetnum = fleet_num
#             bus.unknown_fleetnum_flag = False
#         except KeyError:
#             bus.fleetnum = PLACEHOLDER
#         rtbuslist.append(bus)
        # now - sort that list however we please
#     rtbuslist.sort(key=lambda x: int(x.fleetnum))
#     return template('realtime', time_string=rt.get_data_refreshed_time_str(), rtbuslist=rtbuslist, tripdict=ds.tripdict, stopdict=ds.stopdict, group=group, rdict=rdict)

# @app.route('/bus')
# def bus():
#     return template('error', error='No Bus Specified')

# @app.route('/bus/<number:int>')
# def bus_number(number):
#     if(not businfo.is_known_bus(str(number))):
#         return template('error', error='Unknown Bus {0}'.format(number), message='Is this a new bus?')
#     return template('bus', fleetnum=str(number))

@app.route('/blocks')
def blocks():
    return system_blocks(DEFAULT_SYSTEM_ID)

@app.route('/<system_id>/blocks')
def system_blocks(system_id):
    system = get_system(system_id)
    if system is None:
        return template('templates/invalid_system', systems=all_systems(), system_id=system_id)
    return template('templates/blocks', systems=all_systems(), system=system)

@app.route('/blocks/<block_id:int>')
def blocks_id(block_id):
    return system_blocks_id(DEFAULT_SYSTEM_ID, block_id)

@app.route('/<system_id>/blocks/<block_id:int>')
def system_blocks_id(system_id, block_id):
    system = get_system(system_id)
    if system is None:
        return template('templates/invalid_system', systems=all_systems(), system_id=system_id)
    block = system.get_block(block_id)
    if block is None:
        return template('templates/error', systems=all_systems(), system=system, error=f'Block {block_id} Not Found', message='This block may be from an older version of GTFS which is no longer valid')
    return template('templates/block', systems=all_systems(), system=system, block=block)

@app.route('/trips/<trip_id:int>')
def trips_id(trip_id):
    return system_trips_id(DEFAULT_SYSTEM_ID, trip_id)

@app.route('/<system_id>/trips/<trip_id:int>')
def system_trips_id(system_id, trip_id):
    system = get_system(system_id)
    if system is None:
        return template('templates/invalid_system', systems=all_systems(), system_id=system_id)
    trip = system.get_trip(trip_id)
    if trip is None:
        return template('templates/error', systems=all_systems(), system=system, error=f'Trip {trip_id} Not Found', message='This trip may be from an older version of GTFS which is no longer valid')
    return template('templates/trip', systems=all_systems(), system=system, trip=trip)

@app.route('/stops/<number:int>')
def stops_number(number):
    return system_stops_number(DEFAULT_SYSTEM_ID, number)

@app.route('/<system_id>/stops/<number:int>')
def system_stops_number(system_id, number):
    system = get_system(system_id)
    if system is None:
        return template('templates/invalid_system', systems=all_systems(), system_id=system_id)
    stop = system.get_stop(number=number)
    if stop is None:
        return template('templates/error', systems=all_systems(), system=system, error=f'Stop {number} Not Found')
    return template('templates/stop', systems=all_systems(), system=system, stop=stop)

@app.route('/about')
def about():
    return template('about')
