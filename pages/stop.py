import datastructure as ds
from bottle import template

class TripTime:
    def __init__(self, tripid, stoptime):
        self.stoptime = stoptime
        self.tripid = tripid
        self.trip = ds.tripdict[tripid]

def formatTripList(triptimelist):
    table_html = """<table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
     <tr>
      <th>BlockID</th>
      <th>TripID</th>
      <th>Headsign</th>
      <th>Depart Time</th>
      <th>Day of week</th>
     </tr>
     </thead>
     <tbody>"""
    # triplist.sort(key=ds.trip_to_numseconds)
    try:
        last_hour = int(triptimelist[0].stoptime.split(':')[0])  # get hour
    except IndexError:
        return table_html
    for triptime in triptimelist:
        trip = triptime.trip
        this_hour = int(triptime.stoptime.split(':')[0])
        entry = ''
        if this_hour > last_hour:  # add line breaks on the hours for clarity
            entry += '<td colspan="5"><hr/></td>'
            last_hour = this_hour
        entry += "<tr>\n"
        entry += "<td>" + trip.blockid + "</td>\n"
        entry += '<td><a href="/trips/' + trip.tripid + '">' + trip.tripid + "</a></td>\n"
        entry += "<td>" + trip.headsign + "</td>\n"
        entry += "<td>" + triptime.stoptime + "</td>\n"
        entry += "<td>" + ds.days_of_week_dict[trip.serviceid] + "</td>\n"
        entry += "</tr>\n"
        table_html += entry
    table_html += '</tbody></table>\n'
    return table_html


def tableForDay(day_str, triptimelist):
    rstr = "<br />"
    rstr += "<h3>{0} ({1} Trips):</h3>".format(day_str, len(triptimelist))
    if(len(triptimelist) == 0):
        rstr += "SKIP DATE? <br>"
    rstr += formatTripList(triptimelist)
    return rstr


def stoppage_html(this_stop):
    trip_times = this_stop.triptimes

    # first, make a big dict of DayStr -> list of triptimes
    day_triptimesdict = {}
    for triptime_tuple in trip_times:
        triptime = TripTime(triptime_tuple[0], triptime_tuple[1])
        trip = triptime.trip
        if(ds.days_of_week_dict[trip.serviceid]) == 'INVALID':
            continue
        if(trip.use_alt_day_string):
            keystr = trip.alt_day_string
        else:
            keystr = ds.days_of_week_dict_longname[trip.serviceid]
        if(keystr in day_triptimesdict.keys()):
            day_triptimesdict[keystr].append(triptime)
        else:
            day_triptimesdict[keystr] = [triptime]
    # now - for each key/value in that dict
    gen_html = "<h1>{1}</h1> \n <h2>Bus Stop {0} - Schedule</h2> \n <hr>".format(
        this_stop.stopcode, this_stop.stopname)
    gen_html += template('templates/map.templ', lon=this_stop.stoplon, lat=this_stop.stoplat)
    day_order = []
    for day_str in day_triptimesdict:
        day_order.append(day_str)
    day_order.sort(key = lambda x: ds.service_order_dict.setdefault(day_triptimesdict[x][0].trip.serviceid, 10000)) #sort by first trip's service id, any unfound keys last
    for day_str in day_order:
        gen_html += tableForDay(day_str, day_triptimesdict[day_str])
    return gen_html
