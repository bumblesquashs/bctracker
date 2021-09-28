
class Time:
    
    def __init__(self, time_string):
        if time_string == 'Unknown':
            self.unknown = True
            self.hour = -1
            self.minute = 0
        else:
            self.unknown = False
            time_parts = time_string.split(':')
            
            self.hour = int(time_parts[0])
            self.minute = int(time_parts[1])
            if len(time_parts) > 2:
                self.second = int(time_parts[2])
            else:
                self.second = 0
    
    def __str__(self):
        if self.unknown:
            return 'Unknown'
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'
    
    def __eq__(self, other):
        if self.unknown or other.unknown:
            return False
        return self.hour == other.hour and self.minute == other.minute and self.second == other.second
    
    def __lt__(self, other):
        if self.hour != other.hour:
            return self.hour < other.hour
        if self.minute != other.minute:
            return self.minute < other.minute
        return self.second < other.second
    
    def get_minutes(self, reset_day=True):
        hour = self.hour
        if reset_day and hour >= 24:
            hour -= 24
        return (hour * 60) + self.minute
    
    def get_difference(self, other):
        self_minutes = self.get_minutes(reset_day=False)
        other_minutes = other.get_minutes(reset_day=False)
        difference = abs(self_minutes - other_minutes)
        return '{0:02d}:{1:02d}'.format(difference // 60, difference % 60)

class StopTime:
    def __init__(self, system, stop_id, trip_id, time_string, sequence):
        self.system = system
        self.stop_id = stop_id
        self.trip_id = trip_id
        self.time = Time(time_string)
        self.sequence = sequence
    
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
