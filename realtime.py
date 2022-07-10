
from os import path, rename
from datetime import datetime

import wget

import protobuf.data.gtfs_realtime_pb2 as protobuf

import helpers.overview
import helpers.record
import helpers.transfer

from models.bus import Bus
from models.date import Date
from models.position import Position
from models.time import Time

import database

positions = {}

last_updated = datetime.now()

def update(system):
    '''Downloads realtime data for the given system, then loads it into memory'''
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
        wget.download(system.realtime_url, data_path)
        
        update_positions(system)
        
        print('\nDone!')
        
        last_updated = datetime.now()
    except Exception as e:
        print(f'\nError: Failed to update realtime for {system}')
        print(f'Error message: {e}')

def update_positions(system):
    '''Loads realtime data for the given system into memory'''
    global positions
        
    data_path = f'data/realtime/{system.id}.bin'
    
    data = protobuf.FeedMessage()
    with open(data_path, 'rb') as file:
        data.ParseFromString(file.read())
    positions = {k:v for (k, v) in positions.items() if v.system != system}
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
        positions[bus_number] = Position.from_entity(system, Bus(bus_number), vehicle)

def update_records():
    '''Updates records in the database based on the current realtime data in memory'''
    try:
        today = Date.today()
        now = Time.now()
        for position in positions.values():
            system = position.system
            bus = position.bus
            if bus.number < 0:
                continue
            overview = helpers.overview.find(bus.number)
            trip = position.trip
            if trip is None:
                record_id = None
            else:
                block = trip.block
                if overview is not None and overview.last_record is not None:
                    last_record = overview.last_record
                    if last_record.system != system:
                        helpers.transfer.create(bus, today, last_record.system, system)
                    if last_record.date == today and last_record.block_id == block.id:
                        helpers.record.update(last_record.id, now)
                        trip_ids = helpers.record.find_trip_ids(last_record)
                        if trip.id not in trip_ids:
                            helpers.record.create_trip(last_record.id, trip)
                        continue
                record_id = helpers.record.create(bus, today, system, block, now, trip)
            if overview is None:
                helpers.overview.create(bus, today, system, record_id)
            else:
                helpers.overview.update(overview, today, system, record_id)
        database.commit()
    except Exception as e:
        print(f'Error: Failed to update records')
        print(f'Error message: {e}')

def get_position(bus_number):
    '''Returns the position for a given bus number, or None'''
    if bus_number in positions:
        return positions[bus_number]
    return None

def get_positions(system_id=None):
    '''Returns all positions for a given system ID'''
    if system_id is None:
        return sorted(positions.values())
    return sorted([p for p in positions.values() if p.system.id == system_id])

def last_updated_string():
    '''Returns the date/time that realtime data was last updated'''
    now = datetime.now().date()
    if last_updated.date() == now:
        return last_updated.strftime("at %H:%M")
    if last_updated.year == now.year:
        return last_updated.strftime("%B %-d at %H:%M")
    return last_updated.strftime("%B %-d, %Y at %H:%M")

def validate(system):
    '''Checks that the realtime data for the given system aligns with the current GTFS for that system'''
    if not system.realtime_enabled:
        return True
    for position in [p for p in positions.values() if p.system == system]:
        trip_id = position.trip_id
        if trip_id is None:
            continue
        if position.trip is None:
            trip_id_sections = trip_id.split(':')
            if len(trip_id_sections) == 3:
                trip_block_section = trip_id_sections[2]
                other_trip_block_sections = {t.id.split(':')[2] for t in system.get_trips() if len(t.id.split(':')) == 3}
                if trip_block_section not in other_trip_block_sections:
                    return False
            else:
                return False
    return True
