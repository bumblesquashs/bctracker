
from enum import Enum
import fleetnumber_translation
import models.bus_range as bus_range

class RealtimeStatus(Enum):
    INACTIVE = "Inactive" # this bus is not tracking right 
    UNASSIGNED = "Unassigned" # this bus is tracking but is not assigned to any block
    OFFROUTE = "Offroute" # this bus is assigned to a block but is not "onroute"
    ONROUTE = "Onroute" # this bus is fully on route (all systems go)

class RealtimeVehiclePosition:
    def __init__(self, system, fleet_id, trip_id, route_id, block_id, stop_id, realtime_status, lat, lon):
        self.fleet_id = fleet_id
        self.system = system
        self.trip_id = trip_id
        self.route_id = route_id
        self.block_id = block_id
        self.stop_id = stop_id
        self.realtime_status = realtime_status
        self.lat = lat
        self.lon = lon
        
    def __eq__(self, other):
        return self.fleet_id == other.fleet_id
    
    @property
    def fleet_number(self):
        return ''
        
    @property
    def has_location_data(self):
        return self.lat is not None and self.lon is not None
        
    @property
    def fleet_number(self):
        translation_table = fleetnumber_translation.get_table()
        try:
           return translation_table[self.fleet_id]
        except KeyError:
           return None
           
    @property
    def bus(self):
        if self.fleet_number == None:
            return None
        return bus_range.get(int(self.fleet_number))
        