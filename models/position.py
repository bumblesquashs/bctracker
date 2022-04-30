
import math

from models.time import Time

MINIMUM_MINUTES = 4

class Position:
    __slots__ = ('system', 'bus', 'trip_id', 'stop_id', 'lat', 'lon', 'speed', 'schedule_adherence')
    
    def __init__(self, system, bus, trip_id=None, stop_id=None, lat=None, lon=None, speed=0):
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
            self.schedule_adherence = None
        else:
            self.schedule_adherence = calculate_schedule_adherence(trip, stop, lat, lon)
    
    def __eq__(self, other):
        return self.bus == other.bus
    
    def __lt__(self, other):
        return self.bus < other.bus
    
    @property
    def has_location(self):
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        if self.trip_id is None:
            return None
        return self.system.get_trip(self.trip_id)
    
    @property
    def stop(self):
        if self.stop_id is None:
            return None
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def colour(self):
        trip = self.trip
        if trip is None:
            return '989898'
        return trip.route.colour
    
    @property
    def json_data(self):
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
        schedule_adherence = self.schedule_adherence
        if schedule_adherence is not None:
            data['schedule_adherence'] = schedule_adherence.json_data
        return data
    
def calculate_schedule_adherence(trip, stop, lat, lon):
    departure = trip.get_departure(stop)
    if departure is None:
        return None
    previous_departure = trip.get_previous_departure(departure)
    try:
        expected_scheduled_mins = departure.time.get_minutes()
        
        if previous_departure is not None:
            previous_departure_mins = previous_departure.time.get_minutes()
            time_difference = expected_scheduled_mins - previous_departure_mins
            
            # in the case where we know a previous stop, and its a long gap, do linear interpolation
            if time_difference >= MINIMUM_MINUTES:
                expected_scheduled_mins = previous_departure_mins + linear_interpolate(lat, lon, previous_departure.stop, stop, time_difference)
        
        return ScheduleAdherence(expected_scheduled_mins - Time.now().get_minutes())
    except AttributeError:
        return None

'''
Estimate how far the position is between two stops in minutes...
aka calculate the fraction of distance a point has travelled between two other points.

Another approach might be projecting the vector from previous_stop to lat-lon onto the vector from
previous_stop to next_stop - this probably involves the dot product somewhere.
Instead we simply take the ratio of the (scalar) distances to each one, which should be an ok estimate
This is simpler and avoids weird results when the position is really in an odd spot
'''
def linear_interpolate(lat, lon, previous_stop, next_stop, time_difference):
    previous_stop_dx = lon - previous_stop.lon
    previous_stop_dy = lat - previous_stop.lat
    next_stop_dx = lon - next_stop.lon
    next_stop_dy = lat - next_stop.lat
    
    distance_to_previous_stop = math.sqrt(previous_stop_dx ** 2 + previous_stop_dy ** 2)
    distance_to_next_stop = math.sqrt(next_stop_dx ** 2 + next_stop_dy ** 2)
    
    scalar_sum_of_displacements = distance_to_previous_stop + distance_to_next_stop
    fraction_travelled = distance_to_previous_stop / scalar_sum_of_displacements
    
    return int(fraction_travelled * time_difference)

class ScheduleAdherence:
    __slots__ = ('value', 'status_class', 'description')
    
    def __init__(self, value):
        self.value = value
        
        if value <= -8:
            self.status_class = 'very-behind'
        elif value <= -5:
            self.status_class = 'behind'
        elif value >= 5:
            self.status_class = 'very-ahead'
        elif value >= 3:
            self.status_class = 'ahead'
        else:
            self.status_class = 'on-time'
        
        if value > 0:
            if value == 1:
                self.description = '1 minute ahead of schedule'
            else:
                self.description = f'{value} minutes ahead of schedule'
        elif value < 0:
            value = abs(value)
            if value == 1:
                self.description = '1 minute behind schedule'
            else:
                self.description = f'{value} minutes behind schedule'
        else:
            self.description = 'On schedule'
    
    def __str__(self):
        if self.value > 0:
            return f'+{self.value}'
        return str(self.value)
    
    @property
    def json_data(self):
        return {
            'value': str(self),
            'status_class': self.status_class,
            'description': self.description
        }
