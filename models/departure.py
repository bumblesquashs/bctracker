
from enum import Enum

import helpers.agency
import helpers.departure
import helpers.system

from models.time import Time

class PickupType(Enum):
    '''Options for pickup behaviour for a departure'''
    
    NORMAL = '0'
    UNAVAILABLE = '1'
    PHONE_REQUEST = '2'
    DRIVER_REQUEST = '3'
    
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

class Departure:
    '''An association between a trip and a stop'''
    
    __slots__ = (
        'system',
        'agency',
        'trip_id',
        'sequence',
        'stop_id',
        'time',
        'pickup_type',
        'dropoff_type',
        'timepoint',
        'distance'
    )
    
    @classmethod
    def from_db(cls, row, prefix='departure'):
        '''Returns a departure initialized from the given database row'''
        system = helpers.system.find(row[f'{prefix}_system_id'])
        agency = helpers.agency.find(row[f'{prefix}_agency_id'])
        trip_id = row[f'{prefix}_trip_id']
        sequence = row[f'{prefix}_sequence']
        stop_id = row[f'{prefix}_stop_id']
        time = Time.parse(row[f'{prefix}_time'], system.timezone, agency.accurate_seconds)
        try:
            pickup_type = PickupType(row[f'{prefix}_pickup_type'])
        except:
            pickup_type = PickupType.NORMAL
        try:
            dropoff_type = DropoffType(row[f'{prefix}_dropoff_type'])
        except:
            dropoff_type = DropoffType.NORMAL
        timepoint = row[f'{prefix}_timepoint'] == 1
        distance = row[f'{prefix}_distance']
        return cls(system, agency, trip_id, sequence, stop_id, time, pickup_type, dropoff_type, timepoint, distance)
    
    @property
    def stop(self):
        '''Returns the stop associated with this departure'''
        return self.system.get_stop(stop_id=self.stop_id)
    
    @property
    def trip(self):
        '''Returns the trip associated with this departure'''
        return self.system.get_trip(self.trip_id)
    
    @property
    def pickup_only(self):
        '''Checks if this departure is pickup-only'''
        if self.pickup_type.is_normal:
            return self.trip is not None and self == self.trip.first_departure
        return False
    
    @property
    def dropoff_only(self):
        '''Checks if this departure is dropoff-only'''
        if self.dropoff_type.is_normal:
            return self.trip is not None and self == self.trip.last_departure
        return False
    
    def __init__(self, system, agency, trip_id, sequence, stop_id, time, pickup_type, dropoff_type, timepoint, distance):
        self.system = system
        self.agency = agency
        self.trip_id = trip_id
        self.sequence = sequence
        self.stop_id = stop_id
        self.time = time
        self.pickup_type = pickup_type
        self.dropoff_type = dropoff_type
        self.timepoint = timepoint
        self.distance = distance
    
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
                if self.trip is None or other.trip is None:
                    return False
                if self.trip.route is None or other.trip.route is None:
                    return False
                return self.trip.route < other.trip.route
            return self.time < other.time
    
    def get_json(self):
        '''Returns a representation of this departure in JSON-compatible format'''
        json = {
            'stop': self.stop.get_json(),
            'time': str(self.time)
        }
        if self.trip is not None and self.trip.route is not None:
            json['colour'] = self.trip.route.colour
            json['text_colour'] = self.trip.route.text_colour
        else:
            json['colour'] = '666666'
            json['text_colour'] = 'FFFFFF'
        return json
    
    def find_previous(self):
        '''Returns the previous departure for the trip'''
        return helpers.departure.find(self.system, self.agency, trip=self.trip, sequence=self.sequence - 1)
    
    def find_next(self):
        '''Returns the next departure for the trip'''
        return helpers.departure.find(self.system, self.agency, trip=self.trip, sequence=self.sequence + 1)
