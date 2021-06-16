from enum import Enum

class RealtimeStatus(Enum):
    INACTIVE = "Inactive" # this bus is not tracking right 
    UNASSIGNED = "Unassigned" # this bus is tracking but is not assigned to any block
    OFFROUTE = "Offroute" # this bus is assigned to a block but is not "onroute"
    ONROUTE = "Onroute" # this bus is fully on route (all systems go)

class RealtimeVehiclePosition:
    def __init__(self, system, fleet_id, trip_id, block_id, stop_id, realtime_status, lat, lon):
        self.fleet_id = fleet_id
        self.system = system
        self.trip_id = trip_id
        self.block_id = block_id
        self.stop_id = stop_id
        self.realtime_status = realtime_status
        self.lat = lat
        self.lon = lon
        # print('loaded realtime vehicle: ' + fleet_id + ' ' + trip_id + ' ' + str(block_id) + ' ' + system.name)
        
    def __eq__(self, other):
        return self.fleet_id == other.fleet_id
    
    @property
    def fleet_number(self):
        return ''
        
    @property
    def has_location_data(self):
        return self.lat is not None and self.lon is not None
        
        
        