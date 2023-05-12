
from enum import Enum

import helpers.departure
import helpers.system

from models.time import Time

class PickupType(Enum):
    NORMAL = '0'
    UNAVAILABLE = '1'
    PHONE_REQUEST = '2'
    DRIVER_REQUEST = '3'
    
    def __str__(self):
        if self == PickupType.UNAVAILABLE:
            return 'Drop off only'
        if self == PickupType.PHONE_REQUEST:
            return 'Pick up by phone request only'
        if self == PickupType.DRIVER_REQUEST:
            return 'Pick up by driver request only'
        return ''
    
    @property
    def is_normal(self):
        return self == PickupType.NORMAL

class DropoffType(Enum):
    NORMAL = '0'
    UNAVAILABLE = '1'
    PHONE_REQUEST = '2'
    DRIVER_REQUEST = '3'
    
    def __str__(self):
        if self == DropoffType.UNAVAILABLE:
            return 'Pick up only'
        if self == DropoffType.PHONE_REQUEST:
            return 'Drop off by phone request only'
        if self == DropoffType.DRIVER_REQUEST:
            return 'Drop off by driver request only'
        return ''
    
    @property
    def is_normal(self):
        return self == DropoffType.NORMAL

class Departure:
    '''An association between a trip and a stop'''
    
    __slots__ = ('system', 'trip_id', 'sequence', 'stop_id', 'time', 'pickup_type', 'dropoff_type', 'timepoint', 'distance')
    
    @classmethod
    def from_csv(cls, row, system):
        '''Returns a departure initialized from the given CSV row'''
        trip_id = row['trip_id']
        sequence = int(row['stop_sequence'])
        stop_id = row['stop_id']
        time = Time.parse(row['departure_time'], system.timezone)
        if 'pickup_type' in row:
            pickup_type = PickupType(row['pickup_type'])
        else:
            pickup_type = PickupType.NORMAL
        if 'drop_off_type' in row:
            dropoff_type = DropoffType(row['drop_off_type'])
        else:
            dropoff_type = DropoffType.NORMAL
        if 'timepoint' in row:
            timepoint = row['timepoint'] == '1'
        else:
            timepoint = False
        if 'shape_dist_traveled' in row:
            try:
                distance = int(row['shape_dist_traveled'])
            except:
                distance = None
        else:
            distance = None
        return cls(system, trip_id, sequence, stop_id, time, pickup_type, dropoff_type, timepoint, distance)
    
    @classmethod
    def from_db(cls, row, prefix='departure'):
        system = helpers.system.find(row[f'{prefix}_system_id'])
        trip_id = row[f'{prefix}_trip_id']
        sequence = row[f'{prefix}_sequence']
        stop_id = row[f'{prefix}_stop_id']
        time = Time.parse(row[f'{prefix}_time'], system.timezone)
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
        return cls(system, trip_id, sequence, stop_id, time, pickup_type, dropoff_type, timepoint, distance)
    
    def __init__(self, system, trip_id, sequence, stop_id, time, pickup_type, dropoff_type, timepoint, distance):
        self.system = system
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
                return self.trip.route < other.trip.route
            return self.time < other.time
    
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
        if self.pickup_type.is_normal:
            return self == self.trip.first_departure
        return False
    
    @property
    def dropoff_only(self):
        if self.dropoff_type.is_normal:
            return self == self.trip.last_departure
        return False
    
    @property
    def json(self):
        '''Returns a representation of this departure in JSON-compatible format'''
        return {
            'stop': self.stop.json,
            'time': str(self.time),
            'colour': self.trip.route.colour,
            'text_colour': self.trip.route.text_colour
        }
    
    def load_previous(self):
        return helpers.departure.find(self.system.id, trip_id=self.trip_id, sequence=self.sequence - 1)
    
    def load_next(self):
        return helpers.departure.find(self.system.id, trip_id=self.trip_id, sequence=self.sequence + 1)
