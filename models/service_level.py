
from enum import Enum

from models.time import Time

class ServiceLevel(Enum):
    '''A basic description of the path a trip follows'''
    
    LOCAL = 'Local'
    EXPRESS = 'Express'
    PEAK = 'Peak'
    PEAK_MORNING = 'Morning Peak'
    PEAK_AFTERNOON = 'Afternoon Peak'
    COMMUTER = 'Commuter'
    EVENING = 'Evening'
    NIGHT = 'Night'
    INTERREGIONAL = 'Interregional'
    HEALTH_CONNECTION = 'Health Connection'
    UNKNOWN = 'Unknown'
    
    @classmethod
    def calculate(cls, system, schedule, trips):
        '''Returns a service level based on a schedule and list of trips'''
        if not schedule:
            return cls.UNKNOWN
        lengths = [t.length for t in trips if t.length]
        start_times = [t.start_time for t in trips]
        if lengths and max(lengths) >= 40 and len(schedule.weekdays) <= 3:
            return cls.HEALTH_CONNECTION
        if min(start_times) >= Time(24, 0, 0, system.timezone):
            return cls.NIGHT
        if min(start_times) >= Time(18, 0, 0, system.timezone):
            return cls.EVENING
        morning_cutoff = Time(10, 0, 0, system.timezone)
        afternoon_cutoff = Time(14, 0, 0, system.timezone)
        midday_trips = [t for t in trips if morning_cutoff <= t.start_time < afternoon_cutoff]
        if not midday_trips:
            morning_trips = [t for t in trips if t.start_time < morning_cutoff]
            afternoon_trips = [t for t in trips if t.start_time >= afternoon_cutoff]
            if morning_trips and afternoon_trips:
                morning_directions = {t.direction for t in morning_trips}
                afternoon_directions = {t.direction for t in afternoon_trips}
                if morning_directions.isdisjoint(afternoon_directions):
                    return cls.COMMUTER
                return cls.PEAK
            if morning_trips:
                return cls.PEAK_MORNING
            return cls.PEAK_AFTERNOON
        if lengths and max(lengths) >= 40:
            return cls.INTERREGIONAL
        densities = [t.departure_count / (t.end_time.get_minutes() - t.start_time.get_minutes()) for t in trips]
        if max(densities) <= 1:
            return cls.EXPRESS
        return cls.LOCAL
    
    def __str__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value
