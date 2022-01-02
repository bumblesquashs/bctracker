import realtime

from models.search_result import SearchResult
from models.service import Sheet

class Route:
    def __init__(self, system, route_id, number, name, colour):
        self.system = system
        self.id = route_id
        self.number = number
        self.name = name
        self.colour = colour
        
        self.number_value = int(''.join([d for d in number if d.isdigit()]))
        
        self.trips = []
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
    def sheets(self):
        if self._sheets is None:
            self._sheets = {t.service.sheet for t in self.trips}
        return self._sheets
    
    @property
    def default_sheet(self):
        sheets = self.sheets
        if Sheet.CURRENT in sheets:
            return Sheet.CURRENT
        if Sheet.NEXT in sheets:
            return Sheet.NEXT
        if Sheet.PREVIOUS in sheets:
            return Sheet.PREVIOUS
        return Sheet.UNKNOWN
    
    @property
    def positions(self):
        positions = realtime.get_positions()
        return [p for p in positions if p.system == self.system and p.trip is not None and p.trip.route_id == self.id]
    
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
        self._sheets = None
    
    def get_trips(self, sheet):
        if sheet is None:
            return self.trips
        return [t for t in self.trips if t.service.sheet == sheet]
    
    def get_services(self, sheet):
        return sorted({t.service for t in self.get_trips(sheet)})
    
    def get_headsigns(self, sheet):
        return sorted({str(t) for t in self.get_trips(sheet)})
    
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
