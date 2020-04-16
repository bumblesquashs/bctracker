from bottle import route, run, request, template, Bottle
import datastructure as ds
import realtime as rt
import businfotable as businfo
import scrape_fleetnums as scrape
import sys
import subprocess

from pages.route import routepage_html
from pages.stop import stoppage_html

PLACEHOLDER = '100000'
ds.start()
rt.download_lastest_files()
rt.load_realtime()

homelink = '<a href="/"> Back to Top</a><br>'

footer = """
</body>
</html>
"""

def no(msg):
  return "Not quite: " + msg + "<br>" + homelink
#All this is Static!

def header(title):
  return """
<html>
<head> <title> {0} </title>
</head>
<body>
""".format(title)

lookup_jscript = '''
<script type="text/javascript">
function busLookup() {
      var busid = document.getElementById('busid_f').value;
      window.location = "/bus/" + busid;
  }
</script>
<form onsubmit="busLookup();" action="javascript:void(0);>
  <label for="busid_f">Bus ID:</label><br>
  <input type="text" id="busid_f" name="busid" method="post">
  <input type="submit" value="Lookup">
</form>
'''


#rdict is routeid -> (routenum, routename, routeid)
rdict = ds.routedict

reverse_rdict = {} #route num -> routeid
#build a reverse route table (routenum->routeid)
for route_tuple in rdict.values():
   reverse_rdict[route_tuple[0]] = route_tuple[2]

#build the route table for the index
index_str = header('Victoria GTFS Test!')
index_str += "<b>Welcome to the silly little Victoria GTFS app!</b><br>"
index_str += '<i>Coming soon!</i> Realtime lookup: choose a bus!<br>'
index_str += lookup_jscript
index_str += '<br />'
index_str += '<a href="blocks"> List of blocks </a><br>'
index_str += '<br />'
index_str += '<a href="all-busses"> Realtime: List of active busses </a><br>'
index_str += '<br />'
index_str += '<a href="?rt=reload">Refresh Realtime</a>'
index_str += '<br />'
index_str += '<br />'
for routeid in rdict:
   index_str += '<a href="routes/' + rdict[routeid][0] + '">' + rdict[routeid][0] + ' ' + rdict[routeid][1] + '</a><br>'
index_str += footer


#build the block table for the blocks page - static

btable_html = """<table>
<tr>
  <th>BlockID</th>
  <th>Routes</th>
  <th>Start Time</th>
  <th>Day of week</th>
</tr>"""
blocklist = ds.blockdict.values()
for block in blocklist:

   entry = "<tr>\n"
   entry += '<td><a href="blocks/' + block.blockid + '">' + block.blockid + "</a></td>\n"
   entry += '<td>'
   b_routes = block.get_block_routes()
   for route in b_routes:
      entry += route + ', '
   entry = entry[:-2] #drop the last comma and space
   entry += "</td>"
   entry += "<td>" + block.triplist[0].starttime + "</td>\n"
   entry += "<td>" + ds.days_of_week_dict[block.serviceid] + "</td>\n"
   entry += "</tr>\n"
   btable_html += entry
btable_html += '</table>\n'

#Dynamic functions
#=========================
def genrtbuslist_html():
     rtbuslist = []
     for busid in rt.rtvehicle_dict:
         bus = rt.rtvehicle_dict[busid]
         try:
              fleet_num = rt.id2fleetnum_dict[busid] #if we know the real time translation, add it here
              bus.fleetnum = fleet_num
              bus.unknown_fleetnum_flag = False
         except KeyError:
             bus.fleetnum = PLACEHOLDER
         rtbuslist.append(bus)
         #now - sort that list however we please
     rtbuslist.sort(key = lambda x: (int(x.scheduled)*-1, int(x.fleetnum)))
     return template('pages/realtime.templ',
                           title='All active busses...',
                           time_string=format(rt.get_data_refreshed_time_str()),
                           rtbuslist=rtbuslist,
                           tripdict=ds.tripdict,
                           stopdict=ds.stopdict)

#Web framework code
#========================================
app = Bottle()

@app.route('/test/<name>')
def testpage(name):
    return template('<b>Test page: Hello {{name}}</b>!', name=name)


@app.route('/')
@app.route('/routes')
@app.route('/routes/')
def index():
    if 'rt' in request.query: #for the refresh data thing
        print('Oi! gotta reload')
        rt.download_lastest_files()
        rt.load_realtime()
    return index_str


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
        rt.load_realtime()
    return genrtbuslist_html()

@app.route('/bus/<fleetnum>')
def buspage(fleetnum):
   rstr = header('Bus Lookup')
   rstr += homelink
   rstr += 'Page for bus with fleetnum ' + fleetnum
   rstr += footer
   return rstr

@app.route('/busid/<busid>')
def buspage(busid):
   rstr = header('Bus Lookup')
   rstr += homelink
   rstr += 'Page for bus with internal id ' + busid
   rstr += footer
   return rstr

@app.route('/blocks')
@app.route('/blocks/')
def allblocks():
   rstr = header('List of Blocks') + homelink
   rstr += "\n All of Victoria's blocks: \n<hr>"
   rstr += btable_html
   rstr += footer
   return rstr

@app.route('/admin')
@app.route('/admin/')
def admin():
    return '''
    <html><head><title>Admin tools</title></head><body>
    Click the following to load new data... <br>
    Note: you probably have to restart the app for any of this to take effect <br>
    <a href="/admin/download-gtfs/">Download Latest GTFS-Static Files (Once every 2 weeks?)</a><br>
    <a href="/admin/download-routes/">Download Latest NextRide Routes.json file (Once every 2 weeks?) </a><br>
    <a href="/admin/scrape-fleet/">Scrape Unknown Fleet Numbers via NextRide API </a><br>
    </body></html>
'''

@app.route('/admin/download-gtfs/')
@app.route('/admin/download-gtfs')
def download_gtfs_sp():
    print('Activating subprocess for gtfs download shell script')
    subprocess.run(['./download_new_gtfs.sh'])
    return('Done. <br> <a href="/admin"> Back </a>')

@app.route('/admin/download-routes')
@app.route('/admin/download-routes/')
def download_routes_sp():
    print('Activating subprocess for NrApi Routes json shell script')
    subprocess.run(['./download_new_routes.sh'])
    return('Done. <br> <a href="/admin"> Back </a>')

@app.route('/admin/scrape-fleet')
@app.route('/admin/scrape-fleet/')
def scrape_fleet():
    print('Scraping fleet again')
    scrape.scrape()
    return('Done. <br> <a href="/admin"> Back </a>')
   
@app.route('/blocks/<blockid>')
def blockview(blockid):
  try:
     triplist = ds.blockdict[blockid].triplist
  except KeyError:
     return no("Couldn't find block with blockid " + blockid)
  return template('pages/block.templ',blockid=blockid, triplist=triplist)

@app.route('/trips/<tripid>')
def tripview(tripid):
   try:
      trip = ds.tripdict[tripid]
   except KeyError:
      return no("Couldn't find trip with tripid " + tripid)
   return template('pages/trip.templ',tripid=tripid, trip=trip)

@app.route('/routes/<routenum>')
def routepage(routenum):
   routepage_str = header('Choose a Trip')  + homelink
   routepage_str += "\n All trips for Route " + routenum + " by the time of their first stop\n<hr>"
   try:
        routepage_str += routepage_html(reverse_rdict[routenum])
   except KeyError:
       return no("Couldn't find route: " + str(routenum))
   routepage_str += footer
   return routepage_str

@app.route('/stops/<stopcode>')
def stoppage(stopcode):
   try:
       stop = ds.stopdict[ds.stopcode2stopnum[stopcode]] #grab the stop object from the stopcode
   except KeyError:
       return no("Couldn't find data for stop " + stopcode)
   rstr = header('Stop Schedule') + homelink
   rstr += stoppage_html(stop)
   rstr += footer
   return rstr

run(app, host='192.168.1.93', port=8080)
