import time
import wget
from os import rename, path
from datetime import datetime
from models.realtime_position import RealtimeStatus, RealtimeVehiclePosition
import protobuf.data.gtfs_realtime_pb2 as protobuf_reader
import fleetnumber_translation

class Realtime:
    def __init__(self):
        self.realtime_positions_dict = {}
        self.last_updated_time = time.time()

    def add_realtime_position(self, realtime_position):
        print('adding : ' + realtime_position.fleet_id)
        self.realtime_positions_dict[realtime_position.fleet_id] = realtime_position
        # print(len(self.realtime_positions_dict.values()))

    def reset_realtime_positions(self):
        self.realtime_positions_dict = {}
        
    @property
    def onroute_realtime_positions(self):
        return [pos for pos in self.realtime_positions_dict.values() if pos.realtime_status != RealtimeStatus.UNASSIGNED]
        
    @property
    def realtime_positions(self):
        return self.realtime_positions_dict.values()
        
    @property
    def is_valid(self):
        return True

# Singleton
global_realtime = Realtime()

def get_realtime():
    return global_realtime

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
    fleetnumber_translation.update_table()
        
def load_realtime_updates(realtime_file_path, system):
    class ParsedPosition:
        def __init__(self, vehicle):
            self.vehicle = vehicle
            self.fleet_id = vehicle.vehicle.id
               
    with open(realtime_file_path, 'rb') as vehicle_positions_file:
        feed_message_parser = protobuf_reader.FeedMessage()
        feed_message_parser.ParseFromString(vehicle_positions_file.read())
        
        for vehicle_struct in feed_message_parser.entity:
            try:
                gtfs_vehicle = vehicle_struct.vehicle
            except AttributeError:
                continue
                
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
            
            realtime_position = RealtimeVehiclePosition(
                fleet_id = parsed_vehicle.fleet_id,
                system = system,
                trip_id = parsed_vehicle.trip_id,
                block_id = parsed_vehicle.block_id,
                stop_id = parsed_vehicle.stop_id,
                realtime_status = parsed_vehicle.status,
                lat = parsed_vehicle.lat,
                lon = parsed_vehicle.lon,
            )
            global_realtime.add_realtime_position(realtime_position)
