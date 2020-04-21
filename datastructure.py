from datetime import date

pathprefix = './data/google_transit/'

midday_secs = 43200  # number of secs at midday


tripspath = pathprefix + 'trips.txt'
routespath = pathprefix + 'routes.txt'
stoptimespath = pathprefix + 'stop_times.txt'
stoppath = pathprefix + 'stops.txt'
calendarpath = pathprefix + 'calendar.txt'

# directionid dict
directionid_dict = {'0': 'Outbound', '1': 'Inbound'}

# helper that sorts list of tuples based on the time in their 5th slot


def hms_to_sec(hms):
    (h, m, s) = hms.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def trip_to_numseconds(trip):
    return hms_to_sec(trip.starttime)


def trip_is_before_midday(trip):
    return (trip_to_numseconds(trip) < 43200)

# the first 3 of these are basically just structs


class Stop:
    def __init__(self, stopid, stopcode, stopname):
        self.stopid = stopid
        self.stopcode = stopcode
        self.stopname = stopname
        self.triptimes = []  # list of (tripid, triptime) tuple


class StopTime:
    def __init__(self, tripid, stopid, stopname, departtime, stopseq):
        self.tripid = tripid
        self.stopid = stopid
        self.departtime = departtime
        self.stopseq = stopseq
        self.stopname = stopname


class Trip:
    def __init__(self, tripid, routeid, serviceid, routenum, blockid, headsign, starttime, startstopname, directionid):
        self.tripid = tripid
        self.routeid = routeid
        self.serviceid = serviceid
        self.routenum = routenum
        self.blockid = blockid
        self.headsign = headsign
        self.starttime = starttime
        self.startstopname = startstopname
        self.directionid = directionid
        # When identical weekday/weekend trip and blocks are consolidated, use this
        self.use_alt_day_string = False
        # When identical weekday/weekend trip and blocks are consolidated, use this
        self.alt_day_string = ''
        self.stoplist = []  # list of stoptimetuple


class Block:
    def __init__(self, blockid):
        self.blockid = blockid
        self.triplist = []
        self.serviceid = 0
        # When identical weekday/weekend trip and blocks are consolidated, use this
        self.use_alt_day_string = False
        # When identical weekday/weekend trip and blocks are consolidated, use this
        self.alt_day_string = ''

    def get_block_routes(self):
        unique_routes = []
        for trip in self.triplist:
            if trip.routenum not in unique_routes:
                unique_routes.append(trip.routenum)
        return unique_routes

    def pretty_print(self):
        if(trip_is_before_midday(self.triplist[0])):
            print(days_of_week_dict[self.serviceid] +
                  ' AM Block (id: ' + self.blockid + ')')
        else:
            print(days_of_week_dict[self.serviceid] +
                  ' PM Block (id: ' + self.blockid + ')')
        print('Routes: ' + str(self.get_block_routes()))
        print('================================')
        for trip in self.triplist:
            print(trip.starttime + ' | ' + trip.headsign +
                  ' (Trip ID: ' + trip.tripid + ')')
        print('================================')


# global dicts of all the data, for exporting
blockdict = {}  # dict of block id-> block obj
tripdict = {}  # dict of trip id -> trip info object
route_triplistdict = {}  # dict of route id -> list of trips for that route
routedict = {}  # dict of routeid -> route info tuple
stopcode2stopnum = {}  # dict of stop code -> stopnum
stopdict = {}  # dict of stopid -> stop obj
days_of_week_dict = {}  # service_id -> day of week
days_of_week_dict_longname = {}  # service_id -> day of week long


def get_today_str():
    return str(date.today()).replace('-', '')


today = get_today_str()

# this function is actually the worst - its AWFUL
this_sheet_enddate = ''


def populate_calendar():
    global days_of_week_dict
    global this_sheet_enddate
    days_of_week_dict = {}
    # handle changing columns here too because why not
    with open(calendarpath, 'r') as cal_f:
        colnames = cal_f.readline().rstrip().split(',')
        for line in cal_f:
            items = line.rstrip().split(',')
            start_date = items[colnames.index('start_date')]
            end_date = items[colnames.index('end_date')]
            service_id = items[colnames.index('service_id')]
            if int(start_date) > int(today) or int(end_date) < int(today):
                # This serviceid is NOT for this SHEET... oh boy
                days_of_week_dict[service_id] = 'INVALID'
                days_of_week_dict_longname[service_id] = 'INVALID'
                continue
            this_sheet_enddate = end_date
            ismonday = items[colnames.index('monday')]
            istuesday = items[colnames.index('tuesday')]
            iswednesday = items[colnames.index('wednesday')]
            isthursday = items[colnames.index('thursday')]
            isfriday = items[colnames.index('friday')]
            issaturday = items[colnames.index('saturday')]
            issunday = items[colnames.index('sunday')]
            if(issunday == '1' and issaturday == '1'):
                days_of_week_dict[service_id] = 'Weekends'
                days_of_week_dict_longname[service_id] = 'Weekends'
                continue
            if(ismonday == '1' and istuesday == '1' and iswednesday == '1' and isthursday == '1' and isfriday == '1'):
                days_of_week_dict[service_id] = 'Weekdays'
                days_of_week_dict_longname[service_id] = 'Weekdays'
                continue
            if(ismonday == '1'):
                days_of_week_dict[service_id] = 'Mon'
                days_of_week_dict_longname[service_id] = 'Mondays'
                continue
            if(istuesday == '1'):
                days_of_week_dict[service_id] = 'Tues'
                days_of_week_dict_longname[service_id] = 'Tuesdays'
                continue
            if(iswednesday == '1'):
                days_of_week_dict[service_id] = 'Wed'
                days_of_week_dict_longname[service_id] = 'Wednesdays'
                continue
            if(isthursday == '1'):
                days_of_week_dict[service_id] = 'Thurs'
                days_of_week_dict_longname[service_id] = 'Thursdays'
                continue
            if(isfriday == '1'):
                days_of_week_dict[service_id] = 'Frid'
                days_of_week_dict_longname[service_id] = 'Fridays'
                continue
            if(issaturday == '1'):
                days_of_week_dict[service_id] = 'Sat'
                days_of_week_dict_longname[service_id] = 'Saturdays'
                continue
            if(issunday == '1'):
                days_of_week_dict[service_id] = 'Sun'
                days_of_week_dict_longname[service_id] = 'Sundays'
                continue
            days_of_week_dict[service_id] = 'Special (id: ' + service_id + ')'
            days_of_week_dict_longname[service_id] = 'Special (id: ' + \
                service_id + ')'


# this loads in all the data and sets up the global dicts
def start():
    # this just used internally
    blocklistdict = {}  # dict of block id->list of trips in the block
    firststoptimes_dict = {}  # dict of trip id -> StopTime object
    # list of stop times just used internally
    stoptime_list = []

    # deal with our nasty globals - its nice if they're global, but we want to clear them every time we restart
    global blockdict
    blockdict = {}  # clear it

    # before we start, deal with the days of the week nonsense
    # NOTE: This function is AWFUL
    populate_calendar()

    # first, make a dict of stops with stops.txt
    with open(stoppath, 'r') as stops_f:
        # in the GTFS standard, the column order can CHANGE!!!!
        # list of the column names, column order is in the first line
        colnames = stops_f.readline().split(',')
        for line in stops_f:
            items = line.rstrip().split(',')
            stopid = items[colnames.index('stop_id')]
            stopcode = items[colnames.index('stop_code')]
            stopname = items[colnames.index('stop_name')]
            stopdict[stopid] = Stop(stopid, stopcode, stopname)

    # fill in the backwards dict here
    for stop in stopdict.values():
        stopcode2stopnum[stop.stopcode] = stop.stopid

    # next, make a dict of routes
    with open(routespath, 'r') as routes_f:
        # in the GTFS standard, the column order can CHANGE!!!!
        # list of the column names, column order is in the first line
        colnames = routes_f.readline().split(',')

        for line in routes_f:  # reads only the other lines
            items = line.rstrip().split(',')
            routeid = items[colnames.index('route_id')]
            routenum = items[colnames.index('route_short_name')]
            routename = items[colnames.index('route_long_name')]
            route_tuple = (routenum, routename, routeid)
            routedict[routeid] = route_tuple

    # now, make a dict of tripids -> start of that trip using the stop times
    # also, make a list of stoptime objects that will get used to fill out each trip
    with open(stoptimespath, 'r') as stoptimes:
        colnames = stoptimes.readline().split(',')  # column order is in the first line

        timesdict = {}  # clear it
        for line in stoptimes:
            items = line.rstrip().split(',')
            tripid = items[colnames.index('trip_id')]
            depart_time = items[colnames.index('departure_time')]
            stopid = items[colnames.index('stop_id')]
            stopseq = items[colnames.index('stop_sequence')]
            stopname = stopdict[stopid].stopname

            st = StopTime(tripid=tripid, stopid=stopid, stopname=stopname,
                          departtime=depart_time, stopseq=stopseq)
            # set the trip's depart time as the depart time from the first stop
            if(stopseq == '1'):
                firststoptimes_dict[tripid] = st
            # add this as a stop time object to the stop time list
            stoptime_list.append(st)

    # make a dict of trips, and then a dict of blocks
    with open(tripspath, 'r') as trips:
        colnames = trips.readline().split(',')
        trip_pop_count = 0
        total_trip_count = 0
        for line in trips:
            total_trip_count += 1
            items = line.rstrip().split(',')
            routeid = items[colnames.index('route_id')]
            serviceid = items[colnames.index('service_id')]
            if days_of_week_dict[serviceid] == 'INVALID':
                continue  # skip trips not from this sheet
            trip_pop_count += 1
            tripid = items[colnames.index('trip_id')]
            headsign = items[colnames.index('trip_headsign')]
            directionid = items[colnames.index('direction_id')]
            blockid = items[colnames.index('block_id')]
            routenum = routedict[routeid][0]  # find route number this way
            depart_time = firststoptimes_dict[tripid].departtime
            first_stop_name = firststoptimes_dict[tripid].stopname

            trip_obj = Trip(routeid=routeid, tripid=tripid, blockid=blockid, routenum=routenum, headsign=headsign,
                            starttime=depart_time, startstopname=first_stop_name, serviceid=serviceid, directionid=directionid)
            tripdict[tripid] = trip_obj

            # add this to a block dict to form the block structure
            if blockid in blocklistdict.keys():
                blocklistdict[blockid].append(tripid)
            else:
                blocklistdict[blockid] = [tripid]
    print('Number of trips read: {0} number of valid trips: {1}'.format(
        total_trip_count, trip_pop_count))
    print('Number of blocks read: ' + str(len(blocklistdict.keys())))

    # now, make a block object for each block
    blocklist = []
    for key in blocklistdict:
        new_block = Block(key)
        for tripid in blocklistdict[key]:  # for each trip in this block
            # add that trip tuple to the block object
            new_block.triplist.append(tripdict[tripid])
            # now, sort that trip list
            new_block.triplist.sort(key=trip_to_numseconds)
        # take serviceid of first trip
        new_block.serviceid = new_block.triplist[0].serviceid
        if(len(new_block.triplist) == 0):
            print('Error! this block is empty... (has no trips??)')
            continue
        # update the block list and dict
        blocklist.append(new_block)
        blockdict[key] = new_block

    # fill in the trip objects for the route_triplistdict
    # maintain a list of trips for each routeid
    for trip in tripdict.values():
        if trip.routeid in route_triplistdict:
            route_triplistdict[trip.routeid].append(trip)
        else:
            route_triplistdict[trip.routeid] = [trip]

    print('Beginning trip->stop population...')
    for st in stoptime_list:
        try:
            tripdict[st.tripid].stoplist.append(st)
        except KeyError:  # for handling those stoptimes for trips not in this sheet
            pass
    for trip in tripdict.values():
        # sort the stoplist by stopseq didnt work so use departtime?
        trip.stoplist.sort(key=lambda x: hms_to_sec(x.departtime))

    print('Beginning stop->trip population...')
    for st in stoptime_list:
        # maintain these two lists in parallel (I know, I know...)
        stop = stopdict[st.stopid]
        # check for trips that arent from this sheet - dont want to put those in
        if(st.tripid not in tripdict):
            continue
        stop.triptimes.append((st.tripid, st.departtime))
    for stop in stopdict.values():
        # sort trip tuple list by time
        stop.triptimes.sort(key=lambda x: hms_to_sec(x[1]))

    print('Beginning trip list, block list day-consolidation...')
    # prune the trip and block dicts - consolidate identical weekday blocks

    # done with setup
    print('Backend setup done!')
