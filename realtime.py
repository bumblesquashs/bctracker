from os import path, rename
from datetime import datetime

import wget

import protobuf.data.gtfs_realtime_pb2 as protobuf

from models.bus import Bus
from models.position import Position

positions = {}

last_updated = datetime.now()

def update(system):
    global last_updated
    if not system.realtime_enabled:
        return
    print(f'Updating realtime data for {system}...')
    data_path = f'data/realtime/{system.id}.bin'
    
    try:
        if path.exists(data_path):
            formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
            archives_path = f'archives/realtime/{system.id}_{formatted_date}.bin'
            rename(data_path, archives_path)
        wget.download(f'http://{system.mapstrat_id}.mapstrat.com/current/gtfrealtime_VehiclePositions.bin', data_path)
        
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
            bus_number = int(vehicle.vehicle.id)
        except:
            bus_number = -(index + 1)
        position = Position(system, True, Bus(bus_number))
        try:
            if vehicle.trip.schedule_relationship == 0 and vehicle.trip.trip_id != '':
                position.trip_id = vehicle.trip.trip_id
        except AttributeError: pass
        try:
            if vehicle.stop_id != '':
                position.stop_id = vehicle.stop_id
        except AttributeError: pass
        try:
            position.lat = vehicle.position.latitude
            position.lon = vehicle.position.longitude
            position.speed = int(vehicle.position.speed * 3.6)
        except AttributeError: pass
        positions[bus_number] = position
        position.calculate_schedule_adherence()

def reset_positions(system):
    global positions
    positions = {k:v for (k, v) in positions.items() if v.system != system}
    system.positions = {}

def get_position(bus):
    if bus.number in positions:
        return positions[bus.number]
    return Position(None, False, bus)

def get_positions():
    return positions.values()

def active_buses():
    return [p.bus for p in positions.values()]

def last_updated_string():
    if last_updated.date() == datetime.now().date():
        return last_updated.strftime("at %H:%M")
    return last_updated.strftime("%B %-d, %Y at %H:%M")

def validate(system):
    if not system.realtime_enabled:
        return True
    count = 0
    for position in [p for p in positions.values() if p.system == system]:
        if count == 10:
            return True
        if position.trip_id is None:
            continue
        trip = position.trip
        if trip is None or not trip.service.is_today:
            return False
        count += 1
    return True
