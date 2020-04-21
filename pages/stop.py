import datastructure as ds


class TripTime:
    def __init__(self, tripid, stoptime):
        self.stoptime = stoptime
        self.tripid = tripid
        self.trip = ds.tripdict[tripid]


def formatTripList(triptimelist):
    table_html = """<table>
     <tr>
      <th>BlockID</th>
      <th>TripID</th>
      <th>Headsign</th>
      <th>Depart Time</th>
      <th>Day of week</th>
     </tr>"""
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
    table_html += '</table>\n'
    return table_html


def tableForDay(day_str, triptimelist):
    rstr = "<br />"
    rstr += "<h3>{0} ({1} Trips)</h3>".format(day_str, len(triptimelist))
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
    gen_html = "<h2> View Stop {0} </h2> \n <h3> {1} </h3> \n Stop Schedule:\n<hr>".format(
        this_stop.stopcode, this_stop.stopname)
    for day_str in day_triptimesdict:
        gen_html += tableForDay(day_str, day_triptimesdict[day_str])
    return gen_html
