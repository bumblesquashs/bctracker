from datetime import datetime
import math

import realtime

MINIMUM_MINUTES = 4

class Position:
    def __init__(self, system, active, bus_id):
        self.system = system
        self.active = active
        self.bus_id = bus_id
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
    def bus(self):
        return realtime.get_bus(bus_id=self.bus_id)
    
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
        
        departure = trip.get_departure(stop)
        if departure is None:
            return
        previous_departure = trip.get_previous_departure(departure)
        try:
            expected_scheduled_mins = departure.time.get_minutes()
            
            if previous_departure is not None:
                previous_departure_mins = previous_departure.time.get_minutes()
                time_difference = expected_scheduled_mins - previous_departure_mins
                
                # in the case where we know a previous stop, and its a long gap, do linear interpolation
                if time_difference >= MINIMUM_MINUTES:
                    expected_scheduled_mins = previous_departure_mins + self.linear_interpolate(previous_departure.stop, stop, time_difference)
            
            now = datetime.now()
            current_mins = (now.hour * 60) + now.minute
            self.schedule_adherence = expected_scheduled_mins - current_mins
        except AttributeError:
            pass
    
    '''
    Estimate how far the position is between two stops in minutes...
    aka calculate the fraction of distance a point has travelled between two other points.
    
    Another approach might be projecting the vector from previous_stop to lat-lon onto the vector from
    previous_stop to next_stop - this probably involves the dot product somewhere.
    Instead we simply take the ratio of the (scalar) distances to each one, which should be an ok estimate
    This is simpler and avoids weird results when the position is really in an odd spot
    '''
    def linear_interpolate(self, previous_stop, next_stop, time_difference):
        previous_stop_dx = self.lon - previous_stop.lon
        previous_stop_dy = self.lat - previous_stop.lat
        next_stop_dx = self.lon - next_stop.lon
        next_stop_dy = self.lat - next_stop.lat
        
        distance_to_previous_stop = math.sqrt(previous_stop_dx ** 2 + previous_stop_dy ** 2)
        distance_to_next_stop = math.sqrt(next_stop_dx ** 2 + next_stop_dy ** 2)
        
        scalar_sum_of_displacements = distance_to_previous_stop + distance_to_next_stop
        fraction_travelled = distance_to_previous_stop / scalar_sum_of_displacements
        
        return int(fraction_travelled * time_difference)
