
from datetime import datetime
import csv

from models.block import Block
from models.route import Route
from models.service import Service
from models.shape import Shape
from models.stop import Stop
from models.stop_time import StopTime
from models.trip import Trip

from formatting import format_csv

import gtfs
import realtime

class System:
    def __init__(self, system_id, remote_id, name, supports_realtime):
        self.id = system_id
        self.remote_id = remote_id
        self.name = name
        self.supports_realtime = supports_realtime
        self.feed_version = ''
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.name < other.name
    
    def update_gtfs(self):
        print(f'Updating GTFS data for {self}...')
        gtfs.update(self)
        print('\nDone!')
        self.load_gtfs()

    def load_gtfs(self):
        print(f'Loading GTFS data for {self}...')
        self.load_feed_info()
        self.load_stops()
        self.load_routes()
        self.load_services()
        self.load_shapes()
        self.load_trips()
        self.load_stop_times()
        self.sort_data()
        print('Done!')

    def update_realtime(self):
        if not self.supports_realtime:
            return
        print(f'Updating realtime data for {self}...')
        realtime.update(self)
        print('\nDone!')
        self.load_realtime()
    
    def load_realtime(self):
        print(f'Loading realtime data for {self}...')
        self.load_buses()
        print('Done!')
    
    def validate_gtfs(self):
        for service in self.all_services():
            if service.end_date.date() < datetime.now().date():
                return False
        if self.supports_realtime:
            pass # TODO: Implement realtime validation
        return True
    
    def load_feed_info(self):
        values = self.read_csv('feed_info')[0]
        self.feed_version = values['feed_version']
    
    # Methods for blocks
    def get_block(self, block_id):
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None

    def all_blocks(self):
        return sorted(self.blocks.values())

    # Methods for buses
    def load_buses(self):
        self.buses = {}
        self.buses_by_number = {}

    def get_bus(self, bus_id=None, number=None):
        if bus_id is not None and bus_id in self.buses:
            return self.buses[bus_id]
        if number is not None and number in self.buses_by_number:
            return self.buses_by_number[number]
        return None

    def all_buses(self):
        return sorted(self.buses.values())
    
    # Methods for routes
    def load_routes(self):
        self.routes = {}
        self.routes_by_number = {}
        for values in self.read_csv('routes'):
            route_id = values['route_id']
            number = int(values['route_short_name'])
            name = values['route_long_name']

            route = Route(self, route_id, number, name)

            self.routes[route_id] = route
            self.routes_by_number[number] = route

    def get_route(self, route_id = None, number = None):
        if route_id is not None and route_id in self.routes:
            return self.routes[route_id]
        if number is not None and number in self.routes_by_number:
            return self.routes_by_number[number]
        return None

    def all_routes(self):
        return sorted(self.routes.values())
    
    # Methods for services
    def load_services(self):
        self.services = {}
        for values in self.read_csv('calendar'):
            service_id = values['service_id']
            start_date = format_csv(values['start_date'])
            end_date = format_csv(values['end_date'])
            mon = values['monday'] == '1'
            tue = values['tuesday'] == '1'
            wed = values['wednesday'] == '1'
            thu = values['thursday'] == '1'
            fri = values['friday'] == '1'
            sat = values['saturday'] == '1'
            sun = values['sunday'] == '1'

            self.services[service_id] = Service(self, service_id, start_date, end_date, mon, tue, wed, thu, fri, sat, sun)
        for values in self.read_csv('calendar_dates'):
            service_id = values['service_id']
            exception_type = int(values['exception_type'])

            service = self.get_service(service_id)
            if service is None or exception_type != 1:
                continue
            service.special_service = format_csv(values['date'])

    def get_service(self, service_id):
        if service_id in self.services:
            return self.services[service_id]
        return None
    
    def all_services(self):
        return sorted(self.services.values())
    
    # Methods for shapes
    def load_shapes(self):
        self.shapes = {}
        for values in self.read_csv('shapes'):
            shape_id = values['shape_id']
            lat = float(values['shape_pt_lat'])
            lon = float(values['shape_pt_lon'])
            sequence = int(values['shape_pt_sequence'])

            shape = self.get_shape(shape_id)
            if shape is None:
                shape = Shape(self, shape_id)
                self.shapes[shape_id] = shape
            
            shape.add_point(lat, lon, sequence)
    
    def get_shape(self, shape_id):
        if shape_id in self.shapes:
            return self.shapes[shape_id]
        return None
    
    # Methods for stop times
    def load_stop_times(self):
        for values in self.read_csv('stop_times'):
            stop_id = values['stop_id']
            if stop_id not in self.stops:
                print(f'Invalid stop id: {stop_id}')
                continue
            trip_id = values['trip_id']
            if trip_id not in self.trips:
                print(f'Invalid trip id: {trip_id}')
                continue
            time = values['departure_time']
            sequence = int(values['stop_sequence'])

            stop_time = StopTime(self, stop_id, trip_id, time, sequence)

            stop_time.stop.add_stop_time(stop_time)
            stop_time.trip.add_stop_time(stop_time)

    # Methods for stops
    def load_stops(self):
        self.stops = {}
        self.stops_by_number = {}
        for values in self.read_csv('stops'):
            stop_id = values['stop_id']
            try:
                number = int(values['stop_code'])
            except:
                continue
            name = values['stop_name']
            lat = values['stop_lat']
            lon = values['stop_lon']

            stop = Stop(self, stop_id, number, name, lat, lon)

            self.stops[stop_id] = stop
            self.stops_by_number[number] = stop

    def get_stop(self, stop_id=None, number=None):
        if stop_id is not None and stop_id in self.stops:
            return self.stops[stop_id]
        if number is not None and number in self.stops_by_number:
            return self.stops_by_number[number]
        return None
    
    # Methods for trips
    def load_trips(self):
        self.trips = {}
        self.blocks = {}
        for values in self.read_csv('trips'):
            trip_id = values['trip_id']
            route_id = values['route_id']
            if route_id not in self.routes:
                print(f'Invalid route id: {route_id}')
                continue
            service_id = values['service_id']
            if service_id not in self.services:
                print(f'Invalid service id: {service_id}')
                continue
            block_id = values['block_id']
            if block_id not in self.blocks:
                self.blocks[block_id] = Block(self, block_id, service_id)
            direction_id = int(values['direction_id'])
            shape_id = values['shape_id']
            headsign = values['trip_headsign']

            trip = Trip(self, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign)

            self.trips[trip_id] = trip

            trip.block.add_trip(trip)
            trip.route.add_trip(trip)

    def get_trip(self, trip_id):
        if trip_id in self.trips:
            return self.trips[trip_id]
        return None

    def sort_data(self):
        print('Sorting data...')
        for stop in self.stops.values():
            stop.stop_times = sorted(stop.stop_times)
        for trip in self.trips.values():
            trip.stop_times = sorted(trip.stop_times)
        for route in self.routes.values():
            route.trips = sorted(route.trips)
        for block in self.blocks.values():
            block.trips = sorted(block.trips)

    def read_csv(self, name):
        rows = []
        with open(f'./data/gtfs/{self.id}/{name}.txt', 'r') as file:
            reader = csv.reader(file)
            columns = next(reader)
            for row in reader:
                rows.append(dict(zip(columns, row)))
        return rows

systems = {
    'victoria': System('victoria', 'victoria', 'Victoria', True),
    'nanaimo': System('nanaimo', 'nanaimo', 'Nanaimo', True),
    'cfv': System('cfv', 'central-fraser-valley', 'Central Fraser Valley', False),
    'kamloops': System('kamloops', 'kamloops', 'Kamloops', True)
}

def get_system(system_id):
    if system_id in systems:
        return systems[system_id]
    return None

def all_systems():
    return systems.values()