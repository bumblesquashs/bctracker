import csv

class System:
    __slots__ = ('id', 'name', 'visible', 'gtfs_enabled', 'realtime_enabled', 'current_sheet_only', 'gtfs_url', 'realtime_url', 'realtime_validation_error_count', 'blocks', 'routes', 'routes_by_number', 'services', 'shapes', 'stops', 'stops_by_number', 'trips', 'positions')
    
    def __init__(self, row):
        self.id = row['system_id']
        self.name = row['name']
        self.visible = row['visible'] == '1'
        self.gtfs_enabled = row['gtfs_enabled'] == '1'
        self.realtime_enabled = row['realtime_enabled'] == '1'
        self.current_sheet_only = row['current_sheet_only'] == '1'
        self.gtfs_url = row['gtfs_url']
        self.realtime_url = row['realtime_url']
        
        self.realtime_validation_error_count = 0
        
        self.blocks = {}
        self.routes = {}
        self.routes_by_number = {}
        self.services = {}
        self.shapes = {}
        self.stops = {}
        self.stops_by_number = {}
        self.trips = {}
        self.positions = {}
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return str(self) < str(other)
    
    def get_block(self, block_id):
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None
    
    def get_blocks(self):
        return sorted(self.blocks.values())
    
    def get_route(self, route_id=None, number=None):
        if route_id is not None and route_id in self.routes:
            return self.routes[route_id]
        if number is not None and number in self.routes_by_number:
            return self.routes_by_number[number]
        return None
    
    def get_routes(self):
        return sorted(self.routes.values())
    
    def get_service(self, service_id):
        if service_id in self.services:
            return self.services[service_id]
        return None
    
    def get_services(self):
        return sorted(self.services.values())
    
    def get_shape(self, shape_id):
        if shape_id in self.shapes:
            return self.shapes[shape_id]
        return None
    
    def get_stop(self, stop_id=None, number=None):
        if stop_id is not None and stop_id in self.stops:
            return self.stops[stop_id]
        if number is not None and number in self.stops_by_number:
            return self.stops_by_number[number]
        return None
    
    def get_stops(self):
        return self.stops.values()
    
    def get_trip(self, trip_id):
        if trip_id in self.trips:
            return self.trips[trip_id]
        return None
    
    def get_trips(self):
        return self.trips.values()
    
    def search_routes(self, query):
        routes = self.get_routes()
        results = [r.get_search_result(query) for r in routes]
        return [r for r in results if r.match > 0]
    
    def search_stops(self, query):
        stops = self.get_stops()
        results = [s.get_search_result(query) for s in stops]
        return [r for r in results if r.match > 0]
    
    def sort_data(self):
        for stop in self.stops.values():
            stop.departures.sort()
        for trip in self.trips.values():
            trip.departures.sort()
        for route in self.routes.values():
            route.trips.sort()
        for block in self.blocks.values():
            block.trips.sort()

systems = {}

def load_systems():
    rows = []
    with open(f'./static_data/systems.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    for row in rows:
        system = System(row)
        systems[system.id] = system

def get_system(system_id):
    if system_id is not None and system_id in systems:
        return systems[system_id]
    return None

def get_systems():
    return systems.values()
