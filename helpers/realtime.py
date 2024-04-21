
from os import path, rename, remove
from datetime import datetime

import requests

import protobuf.data.gtfs_realtime_pb2 as protobuf

import helpers.assignment
import helpers.overview
import helpers.position
import helpers.record
import helpers.transfer

from models.date import Date
from models.time import Time

import config
import database

class RealtimeService:
    
    __slots__ = (
        'last_updated_date',
        'last_updated_time'
    )
    
    def __init__(self):
        self.last_updated_date = None
        self.last_updated_time = None
    
    def update(self, system):
        '''Downloads realtime data for the given system and stores it in the database'''
        if not system.realtime_enabled:
            return
        data_path = f'data/realtime/{system.id}.bin'
        
        print(f'Updating realtime data for {system}')
        
        try:
            if path.exists(data_path):
                if config.default.enable_realtime_backups:
                    formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
                    archives_path = f'archives/realtime/{system.id}_{formatted_date}.bin'
                    rename(data_path, archives_path)
                else:
                    remove(data_path)
            data = protobuf.FeedMessage()
            with requests.get(system.realtime_url, timeout=10) as r:
                if config.default.enable_realtime_backups:
                    with open(data_path, 'wb') as f:
                        f.write(r.content)
                data.ParseFromString(r.content)
            helpers.position.default.delete_all(system)
            for index, entity in enumerate(data.entity):
                vehicle = entity.vehicle
                try:
                    vehicle_id = vehicle.vehicle.id
                    vehicle_name_length = system.agency.vehicle_name_length
                    if vehicle_name_length is not None and len(vehicle_id) > vehicle_name_length:
                        vehicle_id = vehicle_id[-vehicle_name_length:]
                    bus_number = int(vehicle_id)
                except:
                    bus_number = -(index + 1)
                helpers.position.default.create(system, bus_number, vehicle)
            self.last_updated_date = Date.today()
            self.last_updated_time = Time.now(accurate_seconds=False)
            system.last_updated_date = Date.today(system.timezone)
            system.last_updated_time = Time.now(system.timezone, system.agency.accurate_seconds)
        except Exception as e:
            print(f'Failed to update realtime for {system}: {e}')
    
    def update_records(self):
        '''Updates records in the database based on the current positions in the database'''
        try:
            for position in helpers.position.default.find_all():
                try:
                    system = position.system
                    bus = position.bus
                    if bus.number < 0:
                        continue
                    date = Date.today(system.timezone)
                    time = Time.now(system.timezone)
                    overview = helpers.overview.default.find(bus.number)
                    trip = position.trip
                    if trip is None:
                        record_id = None
                    else:
                        block = trip.block
                        assignment = helpers.assignment.default.find(system, block)
                        if not assignment or assignment.bus_number != bus.number:
                            helpers.assignment.default.delete_all(system=system, block=block)
                            helpers.assignment.default.delete_all(bus=bus)
                            helpers.assignment.default.create(system, block, bus, date)
                        if overview is not None and overview.last_record is not None:
                            last_record = overview.last_record
                            if last_record.date == date and last_record.block_id == block.id:
                                helpers.record.default.update(last_record, time)
                                trip_ids = helpers.record.default.find_trip_ids(last_record)
                                if trip.id not in trip_ids:
                                    helpers.record.default.create_trip(last_record, trip)
                                continue
                        record_id = helpers.record.default.create(bus, date, system, block, time, trip)
                    if overview is None:
                        helpers.overview.default.create(bus, date, system, record_id)
                    else:
                        helpers.overview.default.update(overview, date, system, record_id)
                        if overview.last_seen_system != system:
                            helpers.transfer.default.create(bus, date, overview.last_seen_system, system)
                except Exception as e:
                    print(f'Failed to update records: {e}')
            database.default.commit()
        except Exception as e:
            print(f'Failed to update records: {e}')
    
    def get_last_updated(self, time_format):
        '''Returns the date/time that realtime data was last updated'''
        date = self.last_updated_date
        time = self.last_updated_time
        if date is None or time is None:
            return 'N/A'
        if date.is_today:
            return f'at {time.format_web(time_format)} {time.timezone_name}'
        return date.format_since()
    
    def validate(self, system):
        '''Checks that the realtime data for the given system aligns with the current GTFS for that system'''
        if not system.realtime_enabled:
            return True
        for position in helpers.position.default.find_all(system):
            trip_id = position.trip_id
            if trip_id is None:
                continue
            if position.trip is None:
                trip_id_sections = trip_id.split(':')
                if len(trip_id_sections) == 3:
                    block_id = trip_id_sections[2]
                    if system.get_block(block_id) is None:
                        return False
                else:
                    return False
        return True

default = RealtimeService()