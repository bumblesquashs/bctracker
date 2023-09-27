import datetime
import math

import helpers.position
from models.bcf_order import BcfOrder
from models.bcf_ferry import BcfFerry
from models.position import Position
from models.time import Time
from helpers.model import find as model_find
from helpers.bcf_scraper import VesselInfo
from helpers.system import find as find_system

bcf_orders = []

TERMINAL_IN_PORT_TOLERANCE_MINOR = 0.005 # lat lon units
TERMINAL_IN_PORT_TOLERANCE_MAJOR = 0.012 # lat lon units

vessel_last_stops = {} # pepperidge farm remembers

# controversial: remember all trips we've already assigned a ferry to, such that we won't assign another ferry to one again?
# Will this help with late night unscheduled extras or really late trips?
already_done_trips = [] 

def reset():
    global vessel_last_stops, already_done_trips
    vessel_last_stops = {}
    already_done_trips = []
    
def check_new_day():
    '''
    Empty out the day's tracking info at 3:45am to 4:00am
    '''
    now = datetime.datetime.now()
    if now.hour == 3 and now.minute > 45:
        reset()
    
def load():
    global bcf_orders, vessel_last_stops, already_done_trips
    vessel_last_stops = {}
    already_done_trips = []
    
    bcf_orders = [
      BcfOrder(['Island Gwawis','Island Kwigwis', "Island K`ulut`a", 'Island Nagalis'], '2020-2021', model_find('island_class')),
      BcfOrder(['Island Aurora','Island Discovery'], '2017-2019', model_find('island_class')),
      BcfOrder(['Spirit of British Columbia', 'Spirit of Vancouver Island'], '1991-1992', model_find('s_class')),
      BcfOrder(['Coastal Renaissance', 'Coastal Inspiration', 'Coastal Celebration'], '2007', model_find('coastal_class')),
      BcfOrder(['Queen of Coquitlam', 'Queen of Cowichan', 'Queen of Alberni'], '1976', model_find('c_class')),
      BcfOrder(['Queen of Oak Bay', 'Queen of Surrey'], '1981', model_find('c_class')),
      BcfOrder(['Queen of New Westminster'], '1964', model_find('nw_class')),
      BcfOrder(['Salish Orca', 'Salish Eagle', 'Salish Raven'], '2016', model_find('salish_class')),
      BcfOrder(['Salish Heron'], '2020', model_find('salish_class')),
      BcfOrder(['Northern Expedition'], '2009', model_find('unclassed')),
      BcfOrder(['Northern Adventure'], '2009', model_find('unclassed')),
      BcfOrder(['Northern Sea Wolf'], '2000', model_find('unclassed')),
      BcfOrder(['Queen of Capilano', 'Queen of Cumberland'], '1991-1992', model_find('i_class')),
      BcfOrder(['Malaspina Sky'], '2008', model_find('i_class')),
      BcfOrder(['Skeena Queen'], '1997', model_find('century_class')),
      BcfOrder(['Quinitsa'], '1977', model_find('q_class')),
      BcfOrder(['Quinsam'], '1982', model_find('q_class')),
      BcfOrder(['Baynes Sound Connector'], '2015', model_find('unclassed')),
      BcfOrder(['Quadra Queen II', 'Tachek'], '1969', model_find('t_class')),
      BcfOrder(['Klitsa', 'Kahloke', 'Kwuna'], '1972-1975', model_find('k_class')),
      BcfOrder(['Kuper'], '1985', model_find('k_class')),
      BcfOrder(["Spirit of Lax Kw' alaams"], '1960', model_find('n_class'))
    ]

def get_order(name):
    for order in bcf_orders:
        if order.contains(name):
            return order
    return None

def all_bcf_orders():
    return bcf_orders
    
def guess_trip(route, departed_stop, departed_time):
    '''
    Strategy - knowing when the trip departed, and from what terminal, we can
    try to guess what departure it was. We can find all the possible departures given the route
    '''
    
    # find the trips from this terminal - should be in order by start time
    possible_trips = [trip for trip in route.get_trips() if trip.first_departure.stop == departed_stop]
    
    # only the ones for today...
    possible_trips = [trip for trip in possible_trips if trip.service.is_today]
    
    # only the ones we haven't assigned a boat to yet (???)
    # possible_trips = [trip for trip in possible_trips if trip not in already_done_trips]
    
    if len(possible_trips) == 0:
        return None
    
    trip_before, trip_after = None, None
    now = Time.now()
    
    # possible trips is sorted... get the trip that should leave before and after now
    for trip in possible_trips:
        if trip.first_departure.time.is_later:
            # Found the first trip after now
            trip_after = trip
            
            # this means, the last trip considered was the last trip scheduled before now
            break
        # well, this one is the latest past trip to be considered
        trip_before = trip
    
    # ok so that's done... now what? check what we found.
    
    if trip_after is None:
        # We're past the last trip of the night; trip_before is the last trip!
        # if we are under way now, then we must be on it... right?
        already_done_trips.append(trip_before)
        return trip_before
        
    if trip_before is None:
        # The first trip was supposed to leave after now!
        # if we are under way now, then we must be on the first trip... right?
        already_done_trips.append(trip_after)
        return trip_after
        
    # ok so we're between trips, the usual case.
    # fortunately, no bcf route is THAT frequent. they're known to leave like 10 mins early,
    # on occasion. walk on cut offs are 10 mins for major routes
    # main idea, if we're within 15 of a future departure, use it, otherwise, use the previous departure
    early_departure_cutoff_mins = 15
    
    trip_after_mins = trip_after.first_departure.time.minute_difference(now)
    
    if trip_after_mins <= early_departure_cutoff_mins:
        # use the next trip
        already_done_trips.append(trip_after)
        return trip_after
        
    # Default to using the previous trip
    already_done_trips.append(trip_before)
    return trip_before
    
def get_route(vessel_info, all_routes):
    '''
        Returns the gtfs route given the vessel info, which contains what
        route number the vessel was tracked on - comes from which picture it
        was found on. Potential trouble for maps with more than one route,
        to be solved later.
    '''
    # TODO: get gtfs route obj from vessel_info.route_number
    
    for route in all_routes:
        # We've made route.number the actual route number during load
        if str(route.number) == str(vessel_info.route_number):
            return route
            
    print(f'BCF: ERROR: vessel {vessel_info.name} on rt {vessel_info.route_number} {vessel_info.route_name} did not match any route in the gtfs')
    return None
    
def get_stop(bcf_vessel, vessel_info, route, terminal_stops):
    '''
    Returns the terminal stop the vessel is at if it is in port
    
    Otherwise, returns None
    '''
        
    if not (vessel_info.status == 'In Port' or vessel_info.status == 'Stopped'):
        return None
        
    for stop in terminal_stops:
        # Quadrature, get distance
        dx = vessel_info.lon - stop.lon
        dy = vessel_info.lat - stop.lat

        distance_to_stop = math.sqrt(dx ** 2 + dy ** 2)
        
        threshold = TERMINAL_IN_PORT_TOLERANCE_MAJOR if vessel_info.is_major else TERMINAL_IN_PORT_TOLERANCE_MINOR
        
        if distance_to_stop < threshold:
            # Bingo! this is the terminal we are in port at, or stopped at
            return stop
        
    print(f'BCF: WARN: its in port or stopped but we didnt find the terminal: {bcf_vessel}')
    # Didn't find any...
    return None
        
def vessel_to_bcf_ferry(vessel_name):
    '''
    Fetch bctracker style vehicle object from vessel_name
    '''
    return BcfFerry(vessel_name, get_order(vessel_name))
    
def heading_to_bearing(heading):
    compass = { 'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180, 'SW': 225, 'W': 270, 'NW': 315 }
    return compass[heading]
    
def create_positions(bcf_vessels, vessel_infos, stops): 
    '''
    Construct the realtime compatible position classes from all our 
    scraped and hardcoded data
    '''
        
    # BCF Gtfs has stops like: 
    # 2505806,,,Quadra Island (Quathiaski Cove) Ferry Terminal,,50.0423489549844,-125.215469745838,,,1,,America/Vancouver,,,0,
    # 2505807,,,Quadra Island (Quathiaski Cove),,50.0423288700402,-125.217744152463,,,0,2505806,,,,0,
    # So two per terminal, but its the one without "Ferry Terminal" that is the one referred to by trips
    legit_terminal_stops = [stop for stop in stops if 'Ferry Terminal' not in stop.number]
    
    system = find_system('bc-ferries')
    all_routes = system.get_routes()
    rt_positions = []
    
    for bcf_vessel, vessel_info in zip(bcf_vessels, vessel_infos):
        # ones that will currently break things - north routes, route 13, denman island
        # hopefully we can fix the denman island situation tho
        forbidden_route_numbers = [11, 13, 21, 22, 26, 28]
        if vessel_info.route_number in forbidden_route_numbers:
            continue
            
        if not vessel_info.lat or not vessel_info.lon:
            continue
            
        print(f'Generating vessel: {bcf_vessel} {bcf_vessel.order} {vessel_info.status} {vessel_info.destination} {vessel_info.route_number}')
        route = get_route(vessel_info, all_routes)
        
        if route is None:
            # We don't know what route its on, weird,
            print(f'BCF: {bcf_vessel} is on unknown route!')
            position = Position(
                system=system,
                bus=bcf_vessel,
                trip_id=None,
                stop_id=None,
                block_id=None,
                route_id=None,
                lat=vessel_info.lat,
                lon=vessel_info.lon,
                bearing=heading_to_bearing(vessel_info.heading),
                speed=vessel_info.speed,
                adherence=None
            )
            rt_positions.append(position)
            continue
            
        stop = get_stop(bcf_vessel, vessel_info, route, legit_terminal_stops)
        
        # Vessel may be in port. update our memory dict
        if stop is not None:
            # Save it in the last stops list
            vessel_last_stops[bcf_vessel.name] = (stop, vessel_info.tracked_time)
            # Then we aren't on a trip
            trip = None
        else:
            # Ok so we aren't tracking at a stop. Then we're under way! 
            # We must be on a trip.
            try:
                departed_stop, departed_time = vessel_last_stops[bcf_vessel.name]
                
                # use departed stop, time and route to guess!
                trip = guess_trip(route, departed_stop, departed_time)

                if trip:
                    print(f'BCF: SUCCESS: guessed trip: {bcf_vessel} on {route} from {departed_stop} to {trip.headsign} at {trip.first_departure.time}')

                    # Oh and report the last stop fwiw
                    stop = vessel_last_stops[bcf_vessel.name][0]
                else:
                    print(f'BCF: WARN: We are not at a terminal, and we do have a last terminal in the dict, but cant guess a trip: {bcf_vessel}')
            except KeyError:
                print(f'BCF: WARN: We are not at a terminal, and we dont have a last terminal in the dict: {bcf_vessel}')
                trip = None
                stop = None
        
        # could add a from_bcf instead of using the yuge constructor
        position = Position(
            system=system,
            bus=bcf_vessel, # adapt pos class to allow vessesls
            trip_id=trip.id if trip is not None else None,
            stop_id=stop.id if stop is not None else None,
            block_id=None,
            route_id=route.id if route is not None else None,
            lat=vessel_info.lat,
            lon=vessel_info.lon,
            bearing=heading_to_bearing(vessel_info.heading),
            speed=vessel_info.speed,
            adherence=None # TODO, can use that adherence class interpolator, the adherence class wants the next stop tho so leverege the route to get that?
        )
        
        rt_positions.append(position)

    return rt_positions
        
        
    
    