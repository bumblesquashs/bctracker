
from datetime import datetime

from models.block import Block
from models.route import Route
from models.service import Service
from models.shape import Shape
from models.stop import Stop
from models.stop_times import StopTime
from models.trip import Trip

class System:
    def __init__(self, system_id, name):
        self.system_id = system_id
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.system_id == other.system_id
    
    def reload(self):
        self.load_stops()
        self.load_routes()
        self.load_services()
        self.load_shapes()
        self.load_trips()
        self.load_stop_times()
    
    # Methods for blocks
    def add_block(self, block_id, service_id):
        self.blocks[block_id] = Block(self, block_id, service_id)

    def get_block(self, block_id):
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None

    def all_blocks(self):
        return self.blocks.values()

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
        return self.buses.values()
    
    # Methods for routes
    def load_routes(self):
        self.routes = {}
        self.routes_by_number = {}
        self.read_csv('routes', self.add_route)
    
    def add_route(self, values):
        route_id = int(values['route_id'])
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
        return self.routes.values()
    
    # Methods for services
    def load_services(self):
        self.services = {}
        self.read_csv('calendar', self.add_service)
        self.read_csv('calendar_dates', self.add_special_service)

    def add_service(self, values):
        service_id = int(values['service_id'])
        mon = values['monday'] == '1'
        tue = values['tuesday'] == '1'
        wed = values['wednesday'] == '1'
        thu = values['thursday'] == '1'
        fri = values['friday'] == '1'
        sat = values['saturday'] == '1'
        sun = values['sunday'] == '1'

        self.services[service_id] = Service(self, service_id, mon, tue, wed, thu, fri, sat, sun)

    def add_special_service(self, values):
        service_id = int(values['service_id'])
        exception_type = int(values['exception_type'])

        service = self.get_service(service_id)
        if service is None or exception_type != 1:
            return
        date_string = values['date']
        date = datetime.strptime(date_string, '%Y%m%d')

        service.special_service = date.strftime('%B %-d, %Y')

    def get_service(self, service_id):
        if service_id in self.services:
            return self.services[service_id]
        return None
    
    # Methods for shapes
    def load_shapes(self):
        self.shapes = {}
        self.read_csv('shapes', self.add_shape)

    def add_shape(self, values):
        shape_id = int(values['shape_id'])
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
        self.read_csv('stop_times', self.add_stop_time)

    def add_stop_time(self, values):
        stop_id = int(values['stop_id'])
        if stop_id not in self.stops:
            print(f'Invalid stop id: {stop_id}')
            return
        trip_id = int(values['trip_id'])
        if trip_id not in self.trips:
            print(f'Invalid trip id: {trip_id}')
            return
        time = values['departure_time']
        sequence = int(values['stop_sequence'])

        stop_time = StopTime(self, stop_id, trip_id, time, sequence)

        stop_time.stop.add_stop_time(stop_time)
        stop_time.trip.add_stop_time(stop_time)

    # Methods for stops
    def load_stops(self):
        self.stops = {}
        self.stops_by_number = {}
        self.read_csv('stops', self.add_stop)

    def add_stop(self, values):
        stop_id = int(values['stop_id'])
        try:
            number = int(values['stop_code'])
        except:
            return
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
        self.read_csv('trips', self.add_trip)

    def add_trip(self, values):
        trip_id = int(values['trip_id'])
        route_id = int(values['route_id'])
        if route_id not in self.routes:
            print(f'Invalid route id: {route_id}')
            return
        service_id = int(values['service_id'])
        if service_id not in self.services:
            print(f'Invalid service id: {service_id}')
            return
        block_id = int(values['block_id'])
        if block_id not in self.blocks:
            self.add_block(block_id, service_id)
        direction_id = int(values['direction_id'])
        shape_id = int(values['shape_id'])
        headsign = values['trip_headsign']

        trip = Trip(self, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign)

        self.trips[trip_id] = trip

        trip.block.add_trip(trip)
        trip.route.add_trip(trip)

    def get_trip(self, trip_id):
        if trip_id in self.trips:
            return self.trips[trip_id]
        return None

    def read_csv(self, name, operation):
        with open(f'./data/gtfs/{self.system_id}/{name}.txt', 'r') as file:
            column_names = file.readline().rstrip().split(',')
            for line in file:
                line_values = line.rstrip().split(',')
                values = {}
                for column in column_names:
                    values[column] = line_values[column_names.index(column)]
                operation(values)
