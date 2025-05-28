
from dataclasses import dataclass, field
from enum import Enum

from models.context import Context
from models.row import Row
from models.time import Time

import repositories

class PickupType(Enum):
    '''Options for pickup behaviour for a departure'''
    
    NORMAL = '0'
    UNAVAILABLE = '1'
    PHONE_REQUEST = '2'
    DRIVER_REQUEST = '3'
    
    @classmethod
    def from_db(cls, value):
        try:
            return cls(value)
        except:
            return cls.NORMAL
    
    def __str__(self):
        if self == PickupType.UNAVAILABLE:
            return 'No pick up'
        if self == PickupType.PHONE_REQUEST:
            return 'Pick up by phone request only'
        if self == PickupType.DRIVER_REQUEST:
            return 'Pick up by driver request only'
        return ''
    
    @property
    def is_normal(self):
        '''Checks if this is a normal pickup'''
        return self == PickupType.NORMAL

class DropoffType(Enum):
    '''Options for dropoff behaviour for a departure'''
    
    NORMAL = '0'
    UNAVAILABLE = '1'
    PHONE_REQUEST = '2'
    DRIVER_REQUEST = '3'
    
    @classmethod
    def from_db(cls, value):
        try:
            return cls(value)
        except:
            return cls.NORMAL
    
    def __str__(self):
        if self == DropoffType.UNAVAILABLE:
            return 'No drop off'
        if self == DropoffType.PHONE_REQUEST:
            return 'Drop off by phone request only'
        if self == DropoffType.DRIVER_REQUEST:
            return 'Drop off by driver request only'
        return ''
    
    @property
    def is_normal(self):
        '''Checks if this is a normal dropoff'''
        return self == DropoffType.NORMAL

@dataclass(slots=True)
class Departure:
    '''An association between a trip and a stop'''
    
    context: Context
    trip_id: str
    sequence: int
    stop_id: str
    time: Time
    pickup_type: PickupType
    dropoff_type: DropoffType
    timepoint: bool
    distance: float | None
    headsign: str | None
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a departure initialized from the given database row'''
        context = row.context()
        trip_id = row['trip_id']
        sequence = row['sequence']
        stop_id = row['stop_id']
        time = Time.parse(row['time'], context.timezone, context.accurate_seconds)
        pickup_type = PickupType.from_db(row['pickup_type'])
        dropoff_type = DropoffType.from_db(row['dropoff_type'])
        timepoint = row['timepoint'] == 1
        distance = row['distance']
        headsign = row['headsign']
        return cls(context, trip_id, sequence, stop_id, time, pickup_type, dropoff_type, timepoint, distance, headsign)
    
    @property
    def stop(self):
        '''Returns the stop associated with this departure'''
        return self.context.system.get_stop(stop_id=self.stop_id)
    
    @property
    def trip(self):
        '''Returns the trip associated with this departure'''
        return self.context.system.get_trip(self.trip_id)
    
    @property
    def pickup_only(self):
        '''Checks if this departure is pickup-only'''
        if self.pickup_type.is_normal:
            return self.trip and self == self.trip.first_departure
        return False
    
    @property
    def dropoff_only(self):
        '''Checks if this departure is dropoff-only'''
        if self.dropoff_type.is_normal:
            return self.trip and self == self.trip.last_departure
        return False
    
    def __str__(self):
        if self.headsign:
            if self.context.prefix_headsigns and self.trip.route:
                return f'{self.trip.route.number} {self.headsign}'
            return self.headsign
        return str(self.trip)
    
    def __eq__(self, other):
        return self.trip_id == other.trip_id and self.sequence == other.sequence
    
    def __lt__(self, other):
        if self.trip_id == other.trip_id:
            return self.sequence < other.sequence
        else:
            if self.time == other.time:
                if self.dropoff_only or other.pickup_only:
                    return True
                if self.pickup_only or other.dropoff_only:
                    return False
                if not self.trip or not other.trip:
                    return False
                if not self.trip.route or not other.trip.route:
                    return False
                return self.trip.route < other.trip.route
            return self.time < other.time
    
    def get_json(self):
        '''Returns a representation of this departure in JSON-compatible format'''
        json = {
            'stop': self.stop.get_json(),
            'time': str(self.time)
        }
        if self.trip and self.trip.route:
            json['colour'] = self.trip.route.colour
            json['text_colour'] = self.trip.route.text_colour
        else:
            json['colour'] = '666666'
            json['text_colour'] = 'FFFFFF'
        return json
    
    def find_previous(self):
        '''Returns the previous departure for the trip'''
        return repositories.departure.find(self.context, trip=self.trip, sequence=self.sequence - 1)
    
    def find_next(self):
        '''Returns the next departure for the trip'''
        return repositories.departure.find(self.context, trip=self.trip, sequence=self.sequence + 1)
