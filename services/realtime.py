
from os import path, rename, remove
from datetime import datetime

import requests

import protobuf.data.gtfs_realtime_pb2 as protobuf

from di import di

from models.date import Date
from models.time import Time

from services import Config, Database, AssignmentService, OverviewService, PositionService, RealtimeService, RecordService, TransferService

class DefaultRealtimeService(RealtimeService):
    
    __slots__ = (
        'config',
        'database',
        'assignment_service',
        'overview_service',
        'position_service',
        'record_service',
        'transfer_service',
        'last_updated_date',
        'last_updated_time'
    )
    
    def __init__(self, **kwargs):
        self.config = kwargs.get('config') or di[Config]
        self.database = kwargs.get('database') or di[Database]
        self.assignment_service = kwargs.get('assignment_service') or di[AssignmentService]
        self.overview_service = kwargs.get('overview_service') or di[OverviewService]
        self.position_service = kwargs.get('position_service') or di[PositionService]
        self.record_service = kwargs.get('record_service') or di[RecordService]
        self.transfer_service = kwargs.get('transfer_service') or di[TransferService]
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
                if self.config.enable_realtime_backups:
                    formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
                    archives_path = f'archives/realtime/{system.id}_{formatted_date}.bin'
                    rename(data_path, archives_path)
                else:
                    remove(data_path)
            data = protobuf.FeedMessage()
            with requests.get(system.realtime_url, timeout=10) as r:
                if self.config.enable_realtime_backups:
                    with open(data_path, 'wb') as f:
                        f.write(r.content)
                data.ParseFromString(r.content)
            self.position_service.delete_all(system)
            for index, entity in enumerate(data.entity):
                vehicle = entity.vehicle
                try:
                    vehicle_id = vehicle.vehicle.id
                    vehicle_name_length = system.agency.vehicle_name_length
                    if vehicle_name_length and len(vehicle_id) > vehicle_name_length:
                        vehicle_id = vehicle_id[-vehicle_name_length:]
                    bus_number = int(vehicle_id)
                except:
                    bus_number = -(index + 1)
                self.position_service.create(system, bus_number, vehicle)
            self.last_updated_date = Date.today()
            self.last_updated_time = Time.now(accurate_seconds=False)
            system.last_updated_date = Date.today(system.timezone)
            system.last_updated_time = Time.now(system.timezone, system.agency.accurate_seconds)
        except Exception as e:
            print(f'Failed to update realtime for {system}: {e}')
    
    def update_records(self):
        '''Updates records in the database based on the current positions in the database'''
        try:
            for position in self.position_service.find_all():
                try:
                    system = position.system
                    bus = position.bus
                    if bus.number < 0:
                        continue
                    date = Date.today(system.timezone)
                    time = Time.now(system.timezone)
                    overview = self.overview_service.find(bus.number)
                    trip = position.trip
                    if trip:
                        block = trip.block
                        assignment = self.assignment_service.find(system, block)
                        if not assignment or assignment.bus_number != bus.number:
                            self.assignment_service.delete_all(system=system, block=block)
                            self.assignment_service.delete_all(bus=bus)
                            self.assignment_service.create(system, block, bus, date)
                        if overview and overview.last_record:
                            last_record = overview.last_record
                            if last_record.date == date and last_record.block_id == block.id:
                                self.record_service.update(last_record, time)
                                trip_ids = self.record_service.find_trip_ids(last_record)
                                if trip.id not in trip_ids:
                                    self.record_service.create_trip(last_record, trip)
                                continue
                        record_id = self.record_service.create(bus, date, system, block, time, trip)
                    else:
                        record_id = None
                    if overview:
                        self.overview_service.update(overview, date, system, record_id)
                        if overview.last_seen_system != system:
                            self.transfer_service.create(bus, date, overview.last_seen_system, system)
                    else:
                        self.overview_service.create(bus, date, system, record_id)
                except Exception as e:
                    print(f'Failed to update records: {e}')
            self.database.commit()
        except Exception as e:
            print(f'Failed to update records: {e}')
    
    def get_last_updated(self, time_format):
        '''Returns the date/time that realtime data was last updated'''
        date = self.last_updated_date
        time = self.last_updated_time
        if not date or not time:
            return 'N/A'
        if date.is_today:
            return f'at {time.format_web(time_format)} {time.timezone_name}'
        return date.format_since()
    
    def validate(self, system):
        '''Checks that the realtime data for the given system aligns with the current GTFS for that system'''
        if not system.realtime_enabled:
            return True
        for position in self.position_service.find_all(system):
            trip_id = position.trip_id
            if not trip_id:
                continue
            if not position.trip:
                trip_id_sections = trip_id.split(':')
                if len(trip_id_sections) == 3:
                    block_id = trip_id_sections[2]
                    if not system.get_block(block_id):
                        return False
                else:
                    return False
        return True
