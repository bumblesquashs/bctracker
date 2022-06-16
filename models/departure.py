
from models.time import Time

class Departure:
    '''An association between a trip and a stop'''
    
    __slots__ = ('system', 'trip_id', 'sequence', 'stop_id', 'time')
    
    @classmethod
    def from_csv(cls, row, system):
        trip_id = row['trip_id']
        sequence = int(row['stop_sequence'])
        stop_id = row['stop_id']
        time = Time.parse(row['departure_time'])
        return cls(system, trip_id, sequence, stop_id, time)
    
    def __init__(self, system, trip_id, sequence, stop_id, time):
        self.system = system
        self.trip_id = trip_id
        self.sequence = sequence
        self.stop_id = stop_id
        self.time = time
    
    def __eq__(self, other):
        return self.trip_id == other.trip_id and self.sequence == other.sequence
    
    def __lt__(self, other):
        if self.trip_id == other.trip_id:
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
    def is_current(self):
        return self.trip.is_current
    
    @property
    def json(self):
        return {
            'stop': self.stop.json,
            'time': str(self.time),
            'colour': self.trip.route.colour
        }
