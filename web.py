#!/usr/bin/env python

import os
import sys
import munch
import signal
import logging
import inspect
import subprocess
import requestlogger
import realtime as rt
import cherrypy as cp
import logging.handlers
import datastructure as ds
import businfotable as businfo
import scrape_fleetnums as scrape
from pages.stop import stoppage_html
from bottle import route, run, request, template, Bottle, static_file

AUTO_RELOAD = True
RELOAD_ENABLED = True


def controlc_handler(sig, frame):
    print('\n')
    munch.stop_cron()
    print('EXITING: Gooodbye Everybody!')
    sys.exit(0)

def restart_server():
    print('\n')
    munch.stop_cron()
    print('RESTARTING: Loading New static GTFS!')
    os.execv(inspect.getfile(lambda: None), sys.argv)

def download_and_restart():
    print('INVALID GTFS: Automatically restarting... (or reload requested?)')
    try:
        subprocess.call(['./download_new_gtfs.sh'], timeout = 45)
    except subprocess.TimeoutExpired:
        try:
            subprocess.call(['./download_new_gtfs.sh'], timeout = 60)
        except subprocess.TimeoutExpired:
            print('WTF: timeout expired twice, guess no connection?')
            controlc_handler()
    subprocess.call(['./download_new_routes.sh'], timeout = 15)
    restart_server()
    print('this should never be seen haha!')



def crontask_handler(sig, frame):
    try:
        valid = munch.munch()
        if((not valid) and AUTO_RELOAD):
            download_and_restart()
    except:
        print('MUNCH: (in sighandler) Hit exception...')
    return

signal.signal(signal.SIGINT, controlc_handler)
signal.signal(signal.SIGUSR1, crontask_handler)

PLACEHOLDER = '100000'
ds.start()
rt.download_lastest_files()
valid = rt.load_realtime()
if(not valid):
    print('ERROR: Not valid on startup... now thats a zinger.')
    print('ERROR: Try running the download new gtfs script and try again')
    print('ERROR: Shutting down.')
    sys.exit(1)
rt.update_last_seen()
munch.start_cron()

# rdict is routeid -> (routenum, routename, routeid)
rdict = ds.routedict
reverse_rdict = {}  # route num -> routeid
# build a reverse route table (routenum->routeid)
for route_tuple in rdict.values():
    reverse_rdict[route_tuple[0]] = route_tuple[2]

# ==============================================================
# Web helper code!
# ==============================================================

#minature rror page
def no(msg):
    return "Not quite: " + msg + "<br>" + '<a href="/"> Back to Top</a><br>'

# header bar for all pages
def header(title_str):
    return template('sections/header.templ', title=title_str)
#footer for all pages
footer = """
</div>
</body>
</html>
"""
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
    return header('All active busses...') + template('pages/realtime.templ',
                    time_string=rt.get_data_refreshed_time_str(),
                    rtbuslist=rtbuslist,
                    tripdict=ds.tripdict,
                    stopdict=ds.stopdict) + footer

# ========================================
# Web framework: assign routes
# ========================================
app = Bottle()

@app.route('/')
def index():
    if 'munch' in request.query:  # for the refresh data thing
        print('Oi! gotta munch')
        valid = munch.munch()
        if((not valid) and AUTO_RELOAD):
            download_and_restart()
    return header('Victoria GTFS Tracker') + template('pages/home.templ', rdict=rdict) + footer

@app.route('/routes')
@app.route('/routes/')
def index():
    return header('All Routes...') + template('pages/routes.templ', rdict=rdict) + footer

@app.route('/history')
@app.route('/history/')
def index():
    return header('Bus history') + template('pages/history.templ') + footer


@app.route('/style.css')
def style():
    return static_file('style.css', root='.')

@app.route('/bus/')
def buspage_root():
    return no('Gotta choose a bus!')

@app.route('/busid/')
def busidpage_root():
    return no('Gotta choose a busid!')

@app.route('/all-busses/')
@app.route('/all-busses')
def all_busses_templ():
    if 'rt' in request.query:
        print('Oi! gotta reload')
        rt.download_lastest_files()
        valid = rt.load_realtime()
        if((not valid) and AUTO_RELOAD):
            download_and_restart()
        rt.update_last_seen()
    return genrtbuslist_html()

@app.route('/bus/<fleetnum>')
def buspage(fleetnum):
    if(not businfo.is_known_bus(fleetnum)):
        return no('Unknown Fleetnumber {0}! Is this a (recent) BC Transit bus?'.format(fleetnum))
    return header('Bus Lookup') + template('pages/bus.templ', fleetnum=fleetnum) + footer

@app.route('/busid/<busid>')
def buspage(busid):
    if(busid not in rt.id2fleetnum_dict):
        return no('Internal id {0} not found! Is this a fleet number instead of an internal id?'.format(busid))
    fleetnum = rt.id2fleetnum_dict[busid]
    if(businfo.get_bus_range(fleetnum).type == businfo.TYPE_UNKNOWN):
        return no('Unknown Fleetnumber {0}! Is this a BC Transit bus?'.format(fleetnum))
    return header('Bus Lookup') + template('pages/bus.templ', fleetnum=fleetnum) + footer

@app.route('/blocks')
@app.route('/blocks/')
def allblocks():
    return header('List of all Blocks') + template('pages/blocks.templ') + footer

@app.route('/admin/reload-server')
def restart():
    print('Attempting to reload the server')
    if(RELOAD_ENABLED):
        download_and_restart()
    return('Lol you should never see this')


@app.route('/blocks/<blockid>')
def blockview(blockid):
    try:
        triplist = ds.blockdict[blockid].triplist
    except KeyError:
        return no("Couldn't find block with blockid " + blockid)
    return header('Table of Trips') + template('pages/block.templ', blockid=blockid, triplist=triplist) + footer

@app.route('/trips/<tripid>')
def tripview(tripid):
    try:
        trip = ds.tripdict[tripid]
    except KeyError:
        return no("Couldn't find trip with tripid " + tripid)
    return header('View trip...') + template('pages/trip.templ', tripid=tripid, trip=trip)

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
    return header('Viewing route' + routenum) + template('pages/route.templ', day_triplistdict=day_triplistdict, day_order=day_order, routenum=routenum, routename=rdict[this_route][1]) + footer

#this page doesnt use a template - TODO: should probably change that
@app.route('/stops/<stopcode>')
def stoppage(stopcode):
    try:
        # grab the stop object from the stopcode
        stop = ds.stopdict[ds.stopcode2stopnum[stopcode]]
    except KeyError:
        return no("Couldn't find data for stop " + stopcode)
    rstr = header('Stop Schedule')
    rstr += stoppage_html(stop)
    rstr += footer
    return rstr

@app.route('/about')
@app.route('/about/')
def about_page():
    return header('About this abomination...') + template('pages/about.templ') + footer

# =================================
# set up server and launch
# =================================

#use cherrypy server - setup logging
def make_access_log(app, filepath, when='d', interval=7, **kwargs):
    if filepath is not None:
        handlers = [logging.handlers.TimedRotatingFileHandler(
        filepath, when, interval, **kwargs)]
    else:
        handlers = [logging.StreamHandler()]
    return requestlogger.WSGILogger(app, handlers, requestlogger.ApacheFormatter())

cp.config.update('server.conf')
cp.tree.graft(make_access_log(app, 'logs/access_log.log'), '/')
cp.log('Whaaat? here we go')
cp.server.start()
