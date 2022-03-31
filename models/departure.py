
from models.time import Time

class Departure:
    __slots__ = ('system', 'stop_id', 'trip_id', 'time', 'sequence')
    
    def __init__(self, system, row):
        self.system = system
        self.stop_id = row['stop_id']
        self.trip_id = row['trip_id']
        self.time = Time(row['departure_time'])
        self.sequence = int(row['stop_sequence'])
    
    def __eq__(self, other):
        return self.stop_id == other.stop_id and self.trip_id == other.trip_id and self.sequence == other.sequence and self.time == other.time
    
    def __lt__(self, other):
        if self.stop_id == other.stop_id and self.trip_id == other.trip_id:
            return self.sequence < other.sequence
        else:
            return self.time < other.time
    
    @property
    def stop(self):
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def trip(self):
        return self.system.get_trip(self.trip_id)
    
    @property
    def json_data(self):
        return {
            'stop': self.stop.json_data,
            'time': str(self.time),
            'colour': self.trip.route.colour
        }
