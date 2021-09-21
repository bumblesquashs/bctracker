from datetime import datetime, timedelta
import math

def get_minutes(hours, minutes):
    return ((hours * 60) + minutes) % 1440 # accounts for stops past midnight

def get_stoptime_minutes(stop_time):
    (stop_hour, stop_minute) = stop_time.time.split(':')
    return get_minutes(int(stop_hour), int(stop_minute))
    
'''
  Estimate how far a bus has gone between two stops in minutes...
  aka calculate the fraction of distane a point has travelled between two other points.

  Another approach might be projecting the vector from stop1 to lat-lon onto the vector from
  stop1 to stop2 - this probably involves the dot product somewhere.
  Instead we simply take the ratio of the (scalar) distances to each one, which should be an ok estimate
  This is simpler and avoids weird results when the bus location is really in an odd spot
'''
def linear_interpolate(stop1, stop2, lat, lon, time_difference):
    stop_1_deltax = lon - stop1.lon
    stop_1_deltay = lat - stop1.lat
    stop_2_deltax = lon - stop2.lon
    stop_2_deltay = lat - stop2.lat

    distance_to_stop_1 = math.sqrt(stop_1_deltax ** 2 + stop_1_deltay ** 2)
    distance_to_stop_2 = math.sqrt(stop_2_deltax ** 2 + stop_2_deltay ** 2)
    
    scalar_sum_of_displacements = distance_to_stop_1 + distance_to_stop_2
    fraction_travelled = distance_to_stop_1 / scalar_sum_of_displacements

    return int(fraction_travelled * time_difference)

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
        MINIMUM_MINUTES = 1
        trip = self.trip
        stop = self.stop

        if trip is None or stop is None:
            return

        stop_time = trip.get_stop_time(stop)
        previous_stop = trip.get_previous_stop(stop_time)
        try:    
            next_stop_time_mins = get_stoptime_minutes(stop_time)
            
            # simply take current stop's scheduled time as the expected time normally
            expected_scheduled_mins = next_stop_time_mins

            if previous_stop is not None:
                prev_stop_time = trip.get_stop_time(previous_stop)
                prev_stop_time_mins = get_stoptime_minutes(prev_stop_time)
                time_difference = next_stop_time_mins - prev_stop_time_mins

                # in the case where we know a previous stop, and its a long gap, do linear interpolation
                if time_difference > MINIMUM_MINUTES:
                    interp_time = linear_interpolate(previous_stop, stop, self.lat, self.lon, time_difference)
                    # print(f'interpolated: next stop name: {stop.name} total time diff: {time_difference} interpolated time: {interp_time}')
                    expected_scheduled_mins = prev_stop_time_mins + interp_time

            now = datetime.now()
            current_mins = get_minutes(now.hour, now.minute)
            self.schedule_adherence = expected_scheduled_mins - current_mins

        except AttributeError:
            pass