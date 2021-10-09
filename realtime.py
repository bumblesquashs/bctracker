from os import path, rename
from datetime import datetime

import json
import wget
import urllib.request as request

import protobuf.data.gtfs_realtime_pb2 as protobuf

from models.bus import Bus
from models.bus_order import is_valid_bus
from models.position import Position

TRANSLATIONS_PATH = "data/realtime/translations.json"

positions = {}

buses_by_id = {}
buses_by_number = {}

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
        update_translations(system)
        
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
    for entity in data.entity:
        vehicle = entity.vehicle
        position = Position(system, True)
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
        except AttributeError: pass
        # print(f'system: {system.id} {vehicle.vehicle.id}')
        try:
            bus_id = f'{system.id}_{vehicle.vehicle.id}'
            positions[bus_id] = position
        except AttributeError: pass
        position.calculate_schedule_adherence()

def update_translations(system):
    with request.urlopen(f'https://nextride.{system.bctransit_id}.bctransit.com/api/Route') as file:
        system_info = json.loads(file.read())
    pattern_ids = ','.join([str(i['patternID']) for i in system_info])
    with request.urlopen(f'https://nextride.{system.bctransit_id}.bctransit.com/api/VehicleStatuses?patternIds={pattern_ids}') as file:
        bus_info = json.load(file)
    for i in bus_info:
        try:
            vehicle_id = i['vehicleId']
            number = int(i['name'])
            if system.vehicle_id_enabled:
                bus_id = f'{system.id}_{vehicle_id}'
            else:
                bus_id = f'{system.id}_{number}' # Sep 27 2021 - Victoria is now using bus numbers as IDs in realtime data
            buses_by_id[bus_id] = number
            buses_by_number[number] = bus_id
        except KeyError:
            print('Error: fleet number (name) or fleet id (vehicleId) missing from bus nextride query bus entry')
    save_translations()

def save_translations():
    translations = {
        'buses_by_id': buses_by_id,
        'buses_by_number': buses_by_number
    }
    with open(TRANSLATIONS_PATH, 'w') as file:
        json.dump(translations, file)

def load_translations():
    global buses_by_id, buses_by_number
    try:
        with open(TRANSLATIONS_PATH, 'r') as file:
            translations = json.load(file)
    except:
        translations = {}
    buses_by_id = translations.get('buses_by_id', {})
    buses_by_number = {int(k):v for k, v in translations.get('buses_by_number', {}).items()}

def get_bus(bus_id=None, number=None):
    if bus_id is not None:
        return Bus(bus_id, buses_by_id.get(bus_id))
    if number is not None and is_valid_bus(number):
        return Bus(buses_by_number.get(number), number)
    return None

def reset_positions(system):
    global positions
    positions = {k:v for (k, v) in positions.items() if v.system != system}

def get_position(bus_id):
    if bus_id is not None and bus_id in positions:
        return positions[bus_id]
    return Position(None, False)

def active_buses():
    return [get_bus(bus_id=id) for id in positions.keys()]

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
