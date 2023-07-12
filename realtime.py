
from os import path, rename
from datetime import datetime

import requests

import protobuf.data.gtfs_realtime_pb2 as protobuf

import helpers.overview
import helpers.position
import helpers.record
import helpers.transfer

from models.bus import Bus
from models.date import Date
from models.position import Position
from models.time import Time

import database

last_updated_date = None
last_updated_time = None

def update(system):
    '''Downloads realtime data for the given system and stores it in the database'''
    global last_updated_date, last_updated_time
    if not system.realtime_enabled:
        return
    data_path = f'data/realtime/{system.id}.bin'
    
    print(f'Updating realtime data for {system}...', end=' ', flush=True)
    
    try:
        if path.exists(data_path):
            formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
            archives_path = f'archives/realtime/{system.id}_{formatted_date}.bin'
            rename(data_path, archives_path)
        data = protobuf.FeedMessage()
        with requests.get(system.realtime_url, timeout=10) as r:
            with open(data_path, 'wb') as f:
                f.write(r.content)
            data.ParseFromString(r.content)
        helpers.position.delete_all(system)
        for index, entity in enumerate(data.entity):
            vehicle = entity.vehicle
            try:
                vehicle_id = vehicle.vehicle.id
                if len(vehicle_id) > 4:
                    vehicle_id = vehicle_id[-4:]
                bus_number = int(vehicle_id)
            except:
                bus_number = -(index + 1)
            helpers.position.create(Position.from_entity(system, Bus(bus_number), vehicle))
        last_updated_date = Date.today('America/Vancouver')
        last_updated_time = Time.now('America/Vancouver', False)
        system.last_updated_date = Date.today(system.timezone)
        system.last_updated_time = Time.now(system.timezone, False)
        print('Done!')
    except Exception as e:
        print('Error!')
        print(f'Failed to update realtime for {system}: {e}')

def update_records():
    '''Updates records in the database based on the current positions in the database'''
    try:
        for position in helpers.position.find_all():
            try:
                system = position.system
                bus = position.bus
                if bus.number < 0:
                    continue
                today = Date.today(system.timezone)
                now = Time.now(system.timezone)
                overview = helpers.overview.find(bus.number)
                trip = position.trip
                if trip is None:
                    record_id = None
                else:
                    block = trip.block
                    if overview is not None and overview.last_record is not None:
                        last_record = overview.last_record
                        if last_record.system != system and not bus.is_test:
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
            except Exception as e:
                print(f'Failed to update records: {e}')
        database.commit()
    except Exception as e:
        print(f'Failed to update records: {e}')

def get_last_updated(time_format):
    '''Returns the date/time that realtime data was last updated'''
    date = last_updated_date
    time = last_updated_time
    if date is None or time is None:
        return 'N/A'
    if date.is_today:
        if time.timezone is None:
            return f'at {time.format_web(time_format)}'
        return f'at {time.format_web(time_format)} {time.timezone_name}'
    return date.format_since

def validate(system):
    '''Checks that the realtime data for the given system aligns with the current GTFS for that system'''
    if not system.realtime_enabled:
        return True
    for position in helpers.position.find_all(system_id=system.id):
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
