import csv

from models.service import Sheet

class System:
    def __init__(self, system_id, name, visible, gtfs_enabled, realtime_enabled, gtfs_url, realtime_url):
        self.id = system_id
        self.name = name
        self.visible = visible
        self.gtfs_enabled = gtfs_enabled
        self.realtime_enabled = realtime_enabled
        self.gtfs_url = gtfs_url
        self.realtime_url = realtime_url
        
        self.realtime_validation_error_count = 0
        
        self.blocks = {}
        self.routes = {}
        self.routes_by_number = {}
        self.services = {}
        self.shapes = {}
        self.stops = {}
        self.stops_by_number = {}
        self.trips = {}
    
    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.name < other.name
    
    def get_block(self, block_id):
        if block_id in self.blocks:
            return self.blocks[block_id]
        return None
    
    def get_blocks(self, sheet):
        if sheet is None:
            return sorted(self.blocks.values())
        return sorted([b for b in self.blocks.values() if sheet in b.sheets])
    
    def get_route(self, route_id=None, number=None):
        if route_id is not None and route_id in self.routes:
            return self.routes[route_id]
        if number is not None and number in self.routes_by_number:
            return self.routes_by_number[number]
        return None
    
    def get_routes(self, sheet):
        if sheet is None:
            return sorted(self.routes.values())
        return sorted([r for r in self.routes.values() if sheet in r.sheets])
    
    def get_service(self, service_id):
        if service_id in self.services:
            return self.services[service_id]
        return None
    
    def get_services(self, sheet):
        if sheet is None:
            return sorted(self.services.values())
        return sorted([s for s in self.services.values() if s.sheet == sheet])
    
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
    
    def get_stops(self, sheet):
        if sheet is None:
            return self.stops.values()
        return [s for s in self.stops.values() if sheet in s.sheets]
    
    def get_trip(self, trip_id):
        if trip_id in self.trips:
            return self.trips[trip_id]
        return None
    
    def get_trips(self, sheet):
        if sheet is None:
            return self.trips.values()
        return [t for t in self.trips.values() if t.service.sheet == sheet]
    
    def search_routes(self, query):
        routes = self.get_routes(Sheet.CURRENT)
        results = [r.get_search_result(query) for r in routes]
        return [r for r in results if r.match > 0]
    
    def search_stops(self, query):
        stops = self.get_stops(Sheet.CURRENT)
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
        system_id = row['system_id']
        name = row['name']
        visible = row['visible'] == '1'
        gtfs_enabled = row['gtfs_enabled'] == '1'
        realtime_enabled = row['realtime_enabled'] == '1'
        gtfs_url = row['gtfs_url']
        realtime_url = row['realtime_url']
        
        systems[system_id] = System(system_id, name, visible, gtfs_enabled, realtime_enabled, gtfs_url, realtime_url)

def get_system(system_id):
    if system_id is not None and system_id in systems:
        return systems[system_id]
    return None

def get_systems():
    return systems.values()
