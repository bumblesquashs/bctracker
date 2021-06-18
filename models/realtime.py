import time
from models.realtime_position import RealtimeStatus, RealtimeVehiclePosition

# Singleton class for holding all the realtime data
class Realtime:
    def __init__(self):
        self.realtime_positions_dict = {}
        self.last_updated_time = time.time()

    def reset_realtime_positions(self):
        self.realtime_positions_dict = {}

    def get_realtime_positions(self, system):
        if system is None:
            return self.realtime_positions_dict.values()
        return [pos for pos in self.realtime_positions_dict.values() if pos.system == system]
    
    @property
    def is_valid(self):
        return True
        
    # Parsing function: Convert gtfs_vehicle structure -> RealtimePosition object
    def parse_realtime_position(self, gtfs_vehicle, system):
        class ParsedPosition:
            def __init__(self, vehicle):
                self.vehicle = vehicle
                self.fleet_id = vehicle.vehicle.id
                   
        parsed_vehicle = ParsedPosition(gtfs_vehicle)            

        # Parse the trips, stops, and blocks
        try:
            parsed_vehicle.trip_id = gtfs_vehicle.trip.trip_id
            
            parsed_vehicle.is_onroute = False
            parsed_vehicle.is_scheduled = False
            parsed_vehicle.block_id = None
            parsed_vehicle.stop_id = None
            
            if gtfs_vehicle.stop_id != '':
                parsed_vehicle.stop_id = gtfs_vehicle.stop_id
                parsed_vehicle.is_onroute = True
            
            if gtfs_vehicle.trip.schedule_relationship == 0 and gtfs_vehicle.trip.trip_id != '':
                trip = system.get_trip(gtfs_vehicle.trip.trip_id)
                if trip is not None:
                    parsed_vehicle.is_scheduled = True
                    parsed_vehicle.block_id = trip.block_id
                
        except AttributeError:
            parsed_vehicle.status = RealtimeStatus.UNASSIGNED
            
        # Try to get the coordinates - if either coordinate is missing, set both to None
        try:
            pos = gtfs_vehicle.position
            parsed_vehicle.lat = pos.latitude
            parsed_vehicle.lon = pos.longitude
        except AttributeError:
            parsed_vehicle.lat = None
            parsed_vehicle.lon = None
         
        # Determine vehicle status
        if parsed_vehicle.is_onroute and parsed_vehicle.is_scheduled:
            parsed_vehicle.status = RealtimeStatus.ONROUTE
        elif parsed_vehicle.is_scheduled:
            parsed_vehicle.status = RealtimeStatus.OFFROUTE
        else:
            parsed_vehicle.status = RealtimeStatus.UNASSIGNED
        
        realtime_position =  RealtimeVehiclePosition(
            fleet_id = parsed_vehicle.fleet_id,
            system = system,
            trip_id = parsed_vehicle.trip_id,
            block_id = parsed_vehicle.block_id,
            stop_id = parsed_vehicle.stop_id,
            realtime_status = parsed_vehicle.status,
            lat = parsed_vehicle.lat,
            lon = parsed_vehicle.lon,
        )
        
        # Add to dictionary
        self.realtime_positions_dict[realtime_position.fleet_id] = realtime_position


# Singleton
global_realtime = Realtime()

def get_realtime():
    return global_realtime
