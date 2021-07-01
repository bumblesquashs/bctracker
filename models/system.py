
class System:
    def __init__(self, system_id, name, supports_realtime, mapstrat_id=None, bctransit_id=None, ):
        self.id = system_id
        self.mapstrat_id = mapstrat_id or system_id
        self.bctransit_id = bctransit_id or system_id
        self.name = name
        self.supports_realtime = supports_realtime
        self.feed_version = ''
        self.realtime_validation_error_count = 0
    
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

    def all_blocks(self):
        return sorted(self.blocks.values())

    def get_route(self, route_id = None, number = None):
        if route_id is not None and route_id in self.routes:
            return self.routes[route_id]
        if number is not None and number in self.routes_by_number:
            return self.routes_by_number[number]
        return None

    def all_routes(self):
        return sorted(self.routes.values())

    def get_service(self, service_id):
        if service_id in self.services:
            return self.services[service_id]
        return None
    
    def all_services(self):
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

    def get_trip(self, trip_id):
        if trip_id in self.trips:
            return self.trips[trip_id]
        return None

    def sort_data(self):
        for stop in self.stops.values():
            stop.stop_times = sorted(stop.stop_times)
        for trip in self.trips.values():
            trip.stop_times = sorted(trip.stop_times)
        for route in self.routes.values():
            route.trips = sorted(route.trips)
        for block in self.blocks.values():
            block.trips = sorted(block.trips)

systems = {
    'cfv': System('cfv', 'Central Fraser Valley', False, bctransit_id='central-fraser-valley'),
    'chilliwack': System('chilliwack', 'Chilliwack', False),
    'comox': System('comox', 'Comox Valley', True, bctransit_id='comox-valley'),
    'kamloops': System('kamloops', 'Kamloops', True),
    'kelowna': System('kelowna', 'Kelowna', True),
    'nanaimo': System('nanaimo', 'Nanaimo', True),
    'prince-george': System('prince-george', 'Prince George', False),
    'squamish': System('squamish', 'Squamish', True),
    'victoria': System('victoria', 'Victoria', True),
    'whistler': System('whistler', 'Whistler', True),
}

def get_system(system_id):
    if system_id is not None and system_id in systems:
        return systems[system_id]
    return None

def all_systems():
    return systems.values()