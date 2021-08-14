from datetime import datetime, timedelta

class Position:
    def __init__(self, system, active):
        self.system = system
        self.active = active
        self.trip_id = None
        self.stop_id = None
        self.lat = None
        self.lon = None
        self.schedule_adherence = None
    
    @property
    def has_location(self):
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        if self.trip_id is None or self.system is None:
            return None
        return self.system.get_trip(self.trip_id)
    
    @property
    def stop(self):
        if self.stop_id is None or self.system is None:
            return None
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def schedule_adherence_string(self):
        adherence = self.schedule_adherence
        if adherence is None:
            return None
        if adherence > 0:
            if adherence == 1:
                return '1 minute ahead of schedule'
            return f'{adherence} minutes ahead of schedule'
        elif adherence < 0:
            adherence = abs(adherence)
            if adherence == 1:
                return '1 minute behind schedule'
            return f'{adherence} minutes behind schedule'
        return 'On schedule'
    
    def calculate_schedule_adherence(self):
        trip = self.trip
        stop = self.stop
        
        if trip is None or stop is None:
            return
        stop_time = trip.get_stop_time(stop)
        if stop_time is None:
            return
        now = datetime.now()
        (stop_hour, stop_minute) = stop_time.time.split(':')
        total = (now.hour * 60) + now.minute
        stop_total = (int(stop_hour) * 60) + int(stop_minute)
        if stop_total >= (1440):
            # Stop is scheduled after midnight - remove 24 hours
            stop_total = stop_total - 1440
        self.schedule_adherence = stop_total - total
