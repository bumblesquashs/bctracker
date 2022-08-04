
from models.adherence import Adherence

class Position:
    '''Current information about a bus' coordinates, trip, and stop'''
    
    __slots__ = ('system', 'bus', 'trip_id', 'stop_id', 'lat', 'lon', 'speed', 'adherence')
    
    @classmethod
    def from_entity(cls, system, bus, data):
        '''Returns a position initialized from the given realtime data'''
        try:
            trip_id = data.trip.trip_id
            if trip_id == '':
                trip_id = None
        except AttributeError:
            trip_id = None
        try:
            stop_id = data.stop_id
            if stop_id == '':
                stop_id = None
        except AttributeError:
            stop_id = None
        try:
            lat = data.position.latitude
            lon = data.position.longitude
        except AttributeError:
            lat = None
            lon = None
        try:
            speed = int(data.position.speed * 3.6)
        except AttributeError:
            speed = None
        return cls(system, bus, trip_id, stop_id, lat, lon, speed)
    
    def __init__(self, system, bus, trip_id, stop_id, lat, lon, speed):
        self.system = system
        self.bus = bus
        self.trip_id = trip_id
        self.stop_id = stop_id
        self.lat = lat
        self.lon = lon
        self.speed = speed
        
        trip = self.trip
        stop = self.stop
        if trip is None or stop is None or lat is None or lon is None:
            self.adherence = None
        else:
            self.adherence = Adherence.calculate(trip, stop, lat, lon)
    
    def __eq__(self, other):
        return self.bus == other.bus
    
    def __lt__(self, other):
        return self.bus < other.bus
    
    @property
    def has_location(self):
        '''Checks if this position has non-null coordinates'''
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        '''Returns the trip associated with this position, or None'''
        if self.trip_id is None:
            return None
        return self.system.get_trip(self.trip_id)
    
    @property
    def stop(self):
        '''Returns the stop associated with this position, or None'''
        if self.stop_id is None:
            return None
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def colour(self):
        '''Returns the route colour associated with this position'''
        trip = self.trip
        if trip is None:
            return '989898'
        return trip.route.colour
    
    @property
    def json(self):
        '''Returns a representation of this position in JSON-compatible format'''
        data = {
            'bus_number': self.bus.number,
            'lon': self.lon,
            'lat': self.lat,
            'colour': self.colour
        }
        trip = self.trip
        if trip is None:
            data['headsign'] = 'Not In Service'
        else:
            data['headsign'] = str(trip).replace("'", '&apos;')
            data['system_id'] = trip.system.id
            data['shape_id'] = trip.shape_id
        adherence = self.adherence
        if adherence is not None:
            data['adherence'] = adherence.json
        return data
