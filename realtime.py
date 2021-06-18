import time
import wget
from os import rename, path
from datetime import datetime
from models.realtime_position import RealtimeStatus, RealtimeVehiclePosition
from models.realtime import get_realtime
import protobuf.data.gtfs_realtime_pb2 as protobuf_reader
import fleetnumber_translation

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
        

# Read the realtime file using protocol buffer compiled code
def load_realtime_updates(realtime_file_path, system):
    with open(realtime_file_path, 'rb') as vehicle_positions_file:
        feed_message_parser = protobuf_reader.FeedMessage()
        feed_message_parser.ParseFromString(vehicle_positions_file.read())
        
    realtime = get_realtime()
    for vehicle_struct in feed_message_parser.entity:
        try:
            gtfs_vehicle = vehicle_struct.vehicle
        except AttributeError:
            continue
        realtime.parse_realtime_position(gtfs_vehicle, system)

    
