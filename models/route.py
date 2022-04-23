
from os.path import commonprefix
from random import randint, seed
from math import sqrt
from colorsys import hls_to_rgb

from models.search_result import SearchResult
from models.service import create_service_group
from models.sheet import create_sheets

class Route:
    __slots__ = ('system', 'id', 'number', 'number_value', 'full_name', 'colour', 'trips', '_auto_name', '_services', '_service_group', '_sheets')
    
    def __init__(self, system, row):
        self.system = system
        self.id = row['route_id']
        self.number = row['route_short_name']
        self.number_value = int(''.join([d for d in self.number if d.isdigit()]))
        if 'route_long_name' in row and row['route_long_name'] != '':
            self.full_name = row['route_long_name']
        else:
            self.full_name = None
        if 'route_color' in row and row['route_color'] != '000000':
            self.colour = row['route_color']
        else:
            # Generate a random colour based on system ID and route number
            seed(system.id)
            h = (randint(1, 360) + (self.number_value * 137.508)) / 360.0
            seed(system.id + self.number)
            l = randint(30, 50) / 100.0
            s = randint(50, 100) / 100.0
            rgb = hls_to_rgb(h, l, s)
            r = int(rgb[0] * 255)
            g = int(rgb[1] * 255)
            b = int(rgb[2] * 255)
            self.colour = f'{r:02x}{g:02x}{b:02x}'
        
        self.trips = []
        self._auto_name = None
        self._services = None
        self._service_group = None
        self._sheets = None
    
    def __str__(self):
        return f'{self.number} {self.name}'
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.number_value < other.number_value
    
    def __gt__(self, other):
        return self.number_value > other.number_value
    
    @property
    def name(self):
        if self.full_name is None:
            if self._auto_name is None:
                headsigns = self.get_headsigns()
                for i in range(len(headsigns)):
                    headsign = headsigns[i].lstrip(self.number).strip(' ')
                    if headsign.startswith('A '):
                        headsign.lstrip('A ')
                    if headsign.startswith('B '):
                        headsign.lstrip('B ')
                    if ' - ' in headsign:
                        headsign = headsign.split(' - ')[0]
                    if '- ' in headsign:
                        headsign = headsign.split('- ')[0]
                    if ' to ' in headsign:
                        headsign = headsign.split(' to ')[0]
                    if ' To ' in headsign:
                        headsign = headsign.split(' To ')[0]
                    if ' via ' in headsign:
                        headsign = headsign.split(' via ')[0]
                    if ' Via ' in headsign:
                        headsign = headsign.split(' Via ')[0]
                    headsigns[i] = headsign.strip(' ')
                prefix = commonprefix(headsigns).strip(' ')
                if len(prefix) < 3:
                    if len(headsigns) > 2:
                        headsigns = [h for h in headsigns if not h.startswith('To ')]
                    self._auto_name = ' / '.join(sorted(set(headsigns)))
                else:
                    self._auto_name = prefix
            return self._auto_name
        return self.full_name
    
    @property
    def services(self):
        if self._services is None:
            self._services = sorted({t.service for t in self.trips})
        return self._services
    
    @property
    def service_group(self):
        if self._service_group is None:
            self._service_group = create_service_group(self.services)
        return self._service_group
    
    @property
    def sheets(self):
        if self._sheets is None:
            self._sheets = create_sheets(self.services)
        return self._sheets
    
    @property
    def is_current(self):
        for service in self.services:
            if self.system.get_sheet(service).is_current:
                return True
        return False
    
    @property
    def json_data(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'colour': self.colour
        }
    
    @property
    def indicator_json_data(self):
        json = []
        trips = sorted(self.trips, key=lambda t: len(t.points), reverse=True)
        trip = trips[0]
        first_point = trip.points[0]
        last_point = trip.points[-1]
        distance = sqrt(((first_point.lat - last_point.lat) ** 2) + ((first_point.lon - last_point.lon) ** 2))
        if distance <= 0.05:
            count = min((len(trip.points) // 500) + 1, 3)
        else:
            count = min(int(distance * 8) + 1, 4)
        size = len(trip.points) // count
        for i in range(count):
            index = (i * size) + (size // 2)
            point = trip.points[index]
            json.append({
                'system_id': self.system.id,
                'number': self.number,
                'name': self.name.replace("'", '&apos;'),
                'colour': self.colour,
                'lat': point.lat,
                'lon': point.lon
            })
        return json
    
    def add_trip(self, trip):
        self.trips.append(trip)
        self._services = None
        self._service_group = None
        self._sheets = None
        self._auto_name = None
    
    def get_trips(self, service_group=None):
        if service_group is None:
            return self.trips
        return [t for t in self.trips if t.service in service_group.services]
    
    def get_headsigns(self, service_group=None):
        return sorted({str(t) for t in self.get_trips(service_group)})
    
    def get_search_result(self, query):
        query = query.lower()
        number = self.number.lower()
        name = str(self).lower()
        match = 0
        if query in number:
            match += (len(query) / len(number)) * 100
            if number.startswith(query):
                match += len(query)
        elif query in name:
            match += (len(query) / len(name)) * 100
            if name.startswith(query):
                match += len(query)
        return SearchResult('route', self.number, self.name, f'routes/{self.number}', match)
