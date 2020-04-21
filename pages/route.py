import datastructure as ds


def no(msg):
  return "Not quite: " + msg + "</body></html>"

def formatTripList(triplist):
     table_html = """<table>
     <tr>
      <th>BlockID</th>
      <th>TripID</th>
      <th>Headsign</th>
      <th>Departure Time</th>
      <th>Departing From...</th>
      <th>Day of week</th>
     </tr>"""
     triplist.sort(key=ds.trip_to_numseconds)
     for trip in triplist:
         entry = "<tr>\n"
         entry += "<td>" + trip.blockid + "</td>\n"
         entry += '<td><a href="/trips/' + trip.tripid + '">' + trip.tripid + "</a></td>\n"
         entry += "<td>" + trip.headsign + "</td>\n"
         entry += "<td>" + trip.starttime + "</td>\n"
         entry += '<td><a href="/stops/' + ds.stopdict[trip.stoplist[0].stopid].stopcode + '">' + trip.startstopname + "</a></td>\n"
         entry += "<td>" + ds.days_of_week_dict[trip.serviceid] + "</td>\n"
         entry += "</tr>\n"
         table_html += entry
     table_html += '</table>\n'
     return table_html

def tableForDay(day_str, trip_list):
    rstr = "<br />"
    rstr += "<h3>{0}</h3>".format(day_str)
    ib_trips = [trip for trip in trip_list if trip.directionid == '0']
    ob_trips = [trip for trip in trip_list if trip.directionid == '1']
    if(len(ob_trips) != 0):
        rstr += "<h4> Outbound Trips ({0}):</h4>".format(len(ob_trips))
        rstr += formatTripList(ob_trips)
    if(len(ib_trips) != 0):
        rstr += '<br />'
        rstr += "<h4> Inbound Trips ({0}):</h4>".format(len(ob_trips))
        rstr += formatTripList(ib_trips)
    return rstr

def routepage_html(this_route):
   try:
       trip_list = ds.route_triplistdict[this_route]
   except:
       return no("Couldn't find data for route " + this_route)
   #first, make a big dict of DayStr -> list of trip
   day_triplistdict = {}
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
   #now - for each key/value in that dict
   gen_html = ''
   for day_str in day_triplistdict:
       gen_html += tableForDay(day_str, day_triplistdict[day_str])
   return gen_html

def routepage2_html(this_route):
    try:
        trip_list = ds.route_triplistdict[this_route]
    except:
        return no("Couldn't find data for route " + this_route)
    #first, make a big dict of DayStr -> list of trip
    day_triplistdict = {}
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
        return template('pages/route.templ', day_triplistdict=day_triplistdict)
