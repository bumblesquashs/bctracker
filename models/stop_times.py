
import formatting

class StopTime:
    def __init__(self, system, stop_id, trip_id, time, sequence):
        self.system = system
        self.stop_id = stop_id
        self.trip_id = trip_id
        self.time = formatting.format_time(time)
        self.seqence = sequence
    
    def __eq__(self, other):
        if self.stop_id == other.stop_id and self.trip_id == other.trip_id:
            return self.seqence == other.sequence
        else:
            return self.time == other.time

    def __lt__(self, other):
        if self.stop_id == other.stop_id and self.trip_id == other.trip_id:
            return self.seqence < other.sequence
        else:
            (sh, sm) = self.time.split(':')
            (oh, om) = other.time.split(':')
            if sh == oh:
                return int(sm) < int(om)
            else:
                return int(sh) < int(oh)
    
    @property
    def stop(self):
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def trip(self):
        return self.system.get_trip(self.trip_id)
