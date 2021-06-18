
import time
from os import rename, path
from datetime import datetime

import wget
import protobuf.data.gtfs_realtime_pb2 as protobuf_reader

from models.realtime_position import RealtimeStatus, RealtimeVehiclePosition
import fleetnumber_translation

# Singleton class for holding all the realtime data
class Realtime:
    def __init__(self):
        self.realtime_positions_dict = {}
        self.last_updated_time = time.time()
        
    @property
    def pretty_last_updated_time(self):
        return time.strftime("%B %-d, %Y at %H:%M", time.localtime(self.last_updated_time))

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
    
# Update the realtime for a system
def update(system):
    if not system.supports_realtime:
        return
    
    system_id = system.id
    remote_id = system.remote_id

    downloads_path = f'downloads/realtime/{system_id}.bin'
    if path.exists(downloads_path):
        formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
        archives_path = f'archives/realtime/{system_id}-{formatted_date}.bin'
        rename(downloads_path, archives_path)
        
    wget.download(f'http://{remote_id}.mapstrat.com/current/gtfrealtime_VehiclePositions.bin', downloads_path)
    load_realtime_updates(downloads_path, system)
    fleetnumber_translation.update_table(system)
    global_realtime.last_updated_time = time.time()

# Read the realtime file using protocol buffer compiled code
def load_realtime_updates(realtime_file_path, system):
    with open(realtime_file_path, 'rb') as vehicle_positions_file:
        feed_message_parser = protobuf_reader.FeedMessage()
        feed_message_parser.ParseFromString(vehicle_positions_file.read())
        
    for vehicle_struct in feed_message_parser.entity:
        try:
            gtfs_vehicle = vehicle_struct.vehicle
        except AttributeError:
            continue
        global_realtime.parse_realtime_position(gtfs_vehicle, system)

