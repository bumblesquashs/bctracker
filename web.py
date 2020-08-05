import munch
import start
import logging
import requestlogger
import realtime as rt
import cherrypy as cp
import history as hist
import logging.handlers
import datastructure as ds
import businfotable as businfo
import scrape_fleetnums as scrape
from pages.stop import stoppage_html
from bottle import route, run, request, template, Bottle, static_file
# miniature error page
def no(msg):
    return "Not quite: " + msg + "<br>" + '<a href="/"> Back to Top</a><br>'

PLACEHOLDER = '100000'
rdict = {}     # rdict is routeid -> (routenum, routename, routeid)
reverse_rdict = {} # route num -> routeid

# Web framework code to start the server
def startup():
    global rdict
    global reverse_rdict
    print('WEB: initializing the web server!')
    rdict = ds.routedict
    # build a reverse route table for handling web requests (routenum->routeid)
    for route_tuple in rdict.values():
        reverse_rdict[route_tuple[0]] = route_tuple[2]
    # Calls to run the bottle code on the cherrypy server
    cp.config.update('server.conf')
    cp.tree.graft(make_access_log(app, 'logs/access_log.log'), '/')
    cp.log('Whaaat? here we go')
    cp.server.start() #That's it for our startup code

# ==============================================================
# Web helper code!
# ==============================================================

# miniature error page
def no(msg):
    return "Not quite: " + msg + "<br>" + '<a href="/"> Back to Top</a><br>'

# header bar for all pages
def header(title_str, include_maps=False):
    return template('templates/header.templ', title=title_str, include_maps=include_maps)

#footer for all pages
def footer():
    return template('templates/footer.templ')

# do some preprocessing when we call the realtime page
def genrtbuslist_html():
    rtbuslist = []
    for busid in rt.rtvehicle_dict:
        bus = rt.rtvehicle_dict[busid]
        try:
            # if we know the real time translation, add it here
            fleet_num = rt.id2fleetnum_dict[busid]
            bus.fleetnum = fleet_num
            bus.unknown_fleetnum_flag = False
        except KeyError:
            bus.fleetnum = PLACEHOLDER
        rtbuslist.append(bus)
        # now - sort that list however we please
    rtbuslist.sort(key=lambda x: (int(x.scheduled) * -1, int(x.fleetnum)))
    return header('Realtime') + template('pages/realtime.templ',
                    time_string=rt.get_data_refreshed_time_str(),
                    rtbuslist=rtbuslist,
                    tripdict=ds.tripdict,
                    stopdict=ds.stopdict) + footer()

def errorPage(error_title, error_message):
    return header('Error') + template('pages/error.templ', error_title=error_title, error_message=error_message) + footer()

# =============================================================
# Web framework: assign routes - its all Server side rendering
# =============================================================
app = Bottle()

@app.route('/style/main.css')
def style_main():
    return static_file('style/main.css', root='.')

@app.route('/style/main-desktop.css')
def style_main():
    return static_file('style/main-desktop.css', root='.')

@app.route('/style/main-mobile.css')
def style_main():
    return static_file('style/main-mobile.css', root='.')

@app.route('/style/tables.css')
def style_tables():
    return static_file('style/tables.css', root='.')

@app.route('/')
def index():
    if 'munch' in request.query:  # for the refresh data thing
        print('Oi! gotta munch')
        valid = munch.munch()
        if((not valid) and start.RELOAD_ENABLED):
            start.download_and_restart()
    return header('BCTracker - Victoria') + template('pages/home.templ', rdict=rdict) + footer()

@app.route('/routes')
@app.route('/routes/')
def routes():
    return header('All Routes') + template('pages/routes.templ', rdict=rdict) + footer()

@app.route('/routes/<routenum>')
def routepage(routenum):
    try:
        this_route = reverse_rdict[routenum]
    except KeyError:
        return no("Couldn't find route: " + str(routenum))
    try:
        trip_list = ds.route_triplistdict[this_route]
    except:
        return ("<html><body>Not quite: Couldn't find data for route " + this_route + "</body></html>")
    # first, make a big dict of DayStr -> list of trip
    day_triplistdict = {}
    day_order = []
    for trip in trip_list:
        if(ds.days_of_week_dict[trip.serviceid]) == 'INVALID':
            continue
        if(trip.use_alt_day_string):
            keystr = trip.alt_day_string
        else:
            keystr = ds.days_of_week_dict_longname[trip.serviceid]
        if(keystr in day_triplistdict.keys()):
            day_triplistdict[keystr].append(trip)
        else:
            day_triplistdict[keystr] = [trip]
    for key in day_triplistdict:
        day_order.append(key)
    day_order.sort(key = lambda x: ds.service_order_dict.setdefault(day_triplistdict[x][0].serviceid, 10000)) #sort by first trip's service id, any unfound keys last
    return header('Route ' + routenum) + template('pages/route.templ', day_triplistdict=day_triplistdict, day_order=day_order, routenum=routenum, routename=rdict[this_route][1]) + footer()

@app.route('/history')
@app.route('/history/')
def history():
    return header('Vehicle History') + template('pages/history.templ') + footer()

@app.route('/realtime')
@app.route('/realtime/')
def realtime():
    if 'rt' in request.query:
        rt.download_lastest_files()
        valid = rt.load_realtime()
        if((not valid) and start.RELOAD_ENABLED):
            start.download_and_restart()
        hist.update_last_seen()
    return genrtbuslist_html()

@app.route('/bus/')
@app.route('/bus/id/')
@app.route('/bus/number/')
def bus():
    return no('Gotta choose a bus!')

@app.route('/bus/id/<busid>')
def busid_number(busid):
    if(busid not in rt.id2fleetnum_dict):
        return errorPage('Bus Not Found', 'Internal ID {0} not found - is this a fleet number instead of an internal ID?'.format(busid))
    fleetnum = rt.id2fleetnum_dict[busid]
    if(businfo.get_bus_range(fleetnum).type == businfo.TYPE_UNKNOWN):
        return no('Unknown Fleetnumber {0}! Is this a BC Transit bus?'.format(fleetnum))
    return header('Bus ' + fleetnum, True) + template('pages/bus.templ', fleetnum=fleetnum) + footer()

@app.route('/bus/number/<fleetnum>')
def bus_number(fleetnum):
    if(not businfo.is_known_bus(fleetnum)):
        return no('Unknown Fleetnumber {0}! Is this a (recent) BC Transit bus?'.format(fleetnum))
    return header('Bus ' + fleetnum, True) + template('pages/bus.templ', fleetnum=fleetnum) + footer()

@app.route('/blocks')
@app.route('/blocks/')
def blocks():
    return header('All Blocks') + template('pages/blocks.templ') + footer()

@app.route('/blocks/<blockid>')
def blocks_number(blockid):
    try:
        triplist = ds.blockdict[blockid].triplist
    except KeyError:
        return no("Couldn't find block with blockid " + blockid)
    return header('Block ' + blockid) + template('pages/block.templ', blockid=blockid, triplist=triplist) + footer()

@app.route('/trips/<tripid>')
def tripview(tripid):
    try:
        trip = ds.tripdict[tripid]
    except KeyError:
        return no("Couldn't find trip with tripid " + tripid)
    return header('Trip ' + tripid) + template('pages/trip.templ', tripid=tripid, trip=trip) + footer()

#this page doesnt use a template - TODO: should probably change that
@app.route('/stops/<stopcode>')
def stoppage(stopcode):
    try:
        # grab the stop object from the stopcode
        stop = ds.stopdict[ds.stopcode2stopnum[stopcode]]
    except KeyError:
        return no("Couldn't find data for stop " + stopcode)
    rstr = header('Stop ' + stopcode, True)
    rstr += stoppage_html(stop)
    rstr += footer()
    return rstr

@app.route('/about')
@app.route('/about/')
def about_page():
    return header('About') + template('pages/about.templ') + footer()

@app.route('/admin/reload-server')
def restart():
    print('Attempting to reload the server')
    if(start.RELOAD_ENABLED):
        start.download_and_restart()
    return('Lol you should never see this')

#use cherrypy server - setup logging
def make_access_log(app, filepath, when='d', interval=7, **kwargs):
    if filepath is not None:
        handlers = [logging.handlers.TimedRotatingFileHandler(
        filepath, when, interval, **kwargs)]
    else:
        handlers = [logging.StreamHandler()]
    return requestlogger.WSGILogger(app, handlers, requestlogger.ApacheFormatter())
