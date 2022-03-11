
from models.order import get_order
import realtime

class Bus:
    __slots__ = ('number')
    
    def __init__(self, bus_number):
        self.number = bus_number
    
    def __str__(self):
        if self.is_unknown:
            return 'Unknown Bus'
        return str(self.number)
    
    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        return self.number == other.number
    
    def __lt__(self, other):
        return self.number < other.number
    
    @property
    def is_unknown(self):
        return self.number < 0
    
    @property
    def order(self):
        return get_order(self)
    
    @property
    def model(self):
        order = self.order
        if order is None:
            return None
        return order.model
    
    @property
    def position(self):
        return realtime.get_position(self)
    
    @property
    def colour(self):
        trip = self.position.trip
        if trip is None:
            return '989898'
        return trip.route.colour
    
    @property
    def json_data(self):
        data = {
            'number': self.number,
            'lon': self.position.lon,
            'lat': self.position.lat,
            'colour': self.colour
        }
        trip = self.position.trip
        if trip is None:
            data['headsign'] = 'Not In Service'
        else:
            data['headsign'] = str(trip).replace("'", '&apos;')
            data['system_id'] = trip.system.id
            data['shape_id'] = trip.shape_id
        schedule_adherence = self.position.schedule_adherence
        if schedule_adherence is not None:
            data['schedule_adherence'] = schedule_adherence.json_data
        return data
