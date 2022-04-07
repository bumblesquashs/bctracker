from os import path, rename
from datetime import datetime

import wget

import protobuf.data.gtfs_realtime_pb2 as protobuf

from models.bus import Bus
from models.position import Position

positions = {}

last_updated = datetime.now()

def update(system):
    global last_updated, positions
    if not system.realtime_enabled:
        return
    print(f'Updating realtime data for {system}...')
    data_path = f'data/realtime/{system.id}.bin'
    
    try:
        if path.exists(data_path):
            formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
            archives_path = f'archives/realtime/{system.id}_{formatted_date}.bin'
            rename(data_path, archives_path)
        wget.download(system.realtime_url, data_path)
        
        positions = {k:v for (k, v) in positions.items() if v.system != system}
        update_positions(system)
        
        print('\nDone!')
        
        last_updated = datetime.now()
    except Exception as e:
        print(f'\nError: Failed to update realtime for {system}')
        print(f'Error message: {e}')

def update_positions(system):
    data_path = f'data/realtime/{system.id}.bin'
    
    data = protobuf.FeedMessage()
    with open(data_path, 'rb') as file:
        data.ParseFromString(file.read())
    for index, entity in enumerate(data.entity):
        vehicle = entity.vehicle
        try:
            vehicle_id = vehicle.vehicle.id
            if len(vehicle_id) > 4:
                vehicle_id = vehicle_id[-4:]
            bus_number = int(vehicle_id)
        except:
            bus_number = -(index + 1)
        if bus_number >= 9990:
            continue
        try:
            trip_id = vehicle.trip.trip_id
            if trip_id == '':
                trip_id = None
        except AttributeError:
            trip_id = None
        try:
            stop_id = vehicle.stop_id
            if stop_id =='':
                stop_id = None
        except AttributeError:
            stop_id = None
        try:
            lat = vehicle.position.latitude
            lon = vehicle.position.longitude
        except AttributeError:
            lat = None
            lon = None
        try:
            speed = int(vehicle.position.speed * 3.6)
        except AttributeError:
            speed = None
        positions[bus_number] = Position(system, Bus(bus_number), trip_id, stop_id, lat, lon, speed)

def get_position(bus_number):
    if bus_number in positions:
        return positions[bus_number]
    return None

def get_positions(system_id=None):
    if system_id is None:
        return sorted(positions.values())
    return sorted([p for p in positions.values() if p.system.id == system_id])

def last_updated_string():
    now = datetime.now().date()
    if last_updated.date() == now:
        return last_updated.strftime("at %H:%M")
    if last_updated.year == now.year:
        return last_updated.strftime("%B %-d at %H:%M")
    return last_updated.strftime("%B %-d, %Y at %H:%M")
