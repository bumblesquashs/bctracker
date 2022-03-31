
from os.path import commonprefix
from random import randint, seed, shuffle

from models.search_result import SearchResult
from models.service import create_service_group
from models.sheet import create_sheets

class Route:
    __slots__ = ('system', 'id', 'number', 'name', 'colour', 'number_value', 'trips', '_auto_name', '_services', '_service_group', '_sheets')
    
    def __init__(self, system, row):
        self.system = system
        self.id = row['route_id']
        self.number = row['route_short_name']
        self.name = row['route_long_name']
        if 'route_color' in row and row['route_color'] != '000000':
            self.colour = row['route_color']
        else:
            # Generate a random colour based on system ID and route number
            seed(system.id + self.number)
            rgb = [randint(0, 100), randint(0, 255), randint(100, 255)]
            shuffle(rgb)
            self.colour = f'{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
        
        self.number_value = int(''.join([d for d in self.number if d.isdigit()]))
        
        self.trips = []
        self._auto_name = None
        self._services = None
        self._service_group = None
        self._sheets = None
    
    def __str__(self):
        if self.name == '':
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
                    self._auto_name = f'{self.number} ' + ' / '.join(sorted(set(headsigns)))
                else:
                    self._auto_name = f'{self.number} {prefix}'
            return self._auto_name
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
    def json_data(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name.replace("'", '&apos;'),
            'colour': self.colour
        }
    
    def add_trip(self, trip):
        self.trips.append(trip)
        self._services = None
        self._service_group = None
        self._sheets = None
    
    def get_trips(self, service_group=None):
        if service_group is None:
            return self.trips
        return [t for t in self.trips if t.service in service_group.services]
    
    def get_headsigns(self, service_group=None):
        return sorted({str(t) for t in self.get_trips(service_group)})
    
    def get_search_result(self, query):
        query = query.lower()
        number = self.number.lower()
        name = self.name.lower()
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
