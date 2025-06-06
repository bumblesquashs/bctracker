
from os import path, rename, remove
from datetime import datetime

import requests

import protobuf.data.gtfs_realtime_pb2 as protobuf

from di import di
from database import Database
from settings import Settings

from models.context import Context
from models.date import Date
from models.time import Time
from models.timestamp import Timestamp

from repositories import AssignmentRepository, OverviewRepository, PositionRepository, RecordRepository, TransferRepository
from services import RealtimeService

class DefaultRealtimeService(RealtimeService):
    
    __slots__ = (
        'database',
        'settings',
        'assignment_repository',
        'overview_repository',
        'position_repository',
        'record_repository',
        'transfer_repository',
        'last_updated'
    )
    
    def __init__(self, database: Database, settings: Settings, **kwargs):
        self.database = database
        self.settings = settings
        self.assignment_repository = kwargs.get('assignment_repository') or di[AssignmentRepository]
        self.overview_repository = kwargs.get('overview_repository') or di[OverviewRepository]
        self.position_repository = kwargs.get('position_repository') or di[PositionRepository]
        self.record_repository = kwargs.get('record_repository') or di[RecordRepository]
        self.transfer_repository = kwargs.get('transfer_repository') or di[TransferRepository]
        self.last_updated = None
    
    def update(self, context: Context):
        '''Downloads realtime data for the given context and stores it in the database'''
        if not context.realtime_enabled:
            return
        data_path = f'data/realtime/{context.system_id}.bin'
        
        print(f'Updating realtime data for {context}')
        
        if path.exists(data_path):
            if self.settings.enable_realtime_backups:
                formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
                archives_path = f'archives/realtime/{context.system_id}_{formatted_date}.bin'
                rename(data_path, archives_path)
            else:
                remove(data_path)
        data = protobuf.FeedMessage()
        with requests.get(context.system.realtime_url, timeout=10) as r:
            if self.settings.enable_realtime_backups:
                with open(data_path, 'wb') as f:
                    f.write(r.content)
            data.ParseFromString(r.content)
        self.position_repository.delete_all(context)
        for index, entity in enumerate(data.entity):
            vehicle = entity.vehicle
            try:
                vehicle_id = vehicle.vehicle.id
                vehicle_name_length = context.vehicle_name_length
                if vehicle_name_length and len(vehicle_id) > vehicle_name_length:
                    vehicle_id = vehicle_id[-vehicle_name_length:]
                bus_number = int(vehicle_id)
            except:
                bus_number = -(index + 1)
            self.position_repository.create(context, bus_number, vehicle)
        self.last_updated = Timestamp.now(accurate_seconds=False)
        context.system.last_updated = Timestamp.now(context.timezone, context.accurate_seconds)
    
    def update_records(self):
        '''Updates records in the database based on the current positions in the database'''
        for position in self.position_repository.find_all():
            try:
                context = position.context
                bus = position.bus
                if bus.number < 0:
                    continue
                date = Date.today(context.timezone)
                time = Time.now(context.timezone)
                overview = self.overview_repository.find(bus.number)
                trip = position.trip
                if trip:
                    block = trip.block
                    assignment = self.assignment_repository.find(context, block)
                    if not assignment or assignment.bus_number != bus.number:
                        self.assignment_repository.delete_all(context, block=block)
                        self.assignment_repository.delete_all(Context(), bus=bus)
                        self.assignment_repository.create(context, block, bus, date)
                    if overview and overview.last_record:
                        last_record = overview.last_record
                        if last_record.date == date and last_record.block_id == block.id:
                            self.record_repository.update(last_record, time)
                            trip_ids = self.record_repository.find_trip_ids(last_record)
                            if trip.id not in trip_ids:
                                self.record_repository.create_trip(last_record, trip)
                            continue
                    record_id = self.record_repository.create(context, bus, date, block, time, trip)
                else:
                    record_id = None
                if overview:
                    self.overview_repository.update(context, overview, date, record_id)
                    if overview.last_seen_context != context:
                        self.transfer_repository.create(bus, date, overview.last_seen_context, context)
                else:
                    self.overview_repository.create(context, bus, date, record_id)
            except Exception as e:
                print(f'Failed to update records: {e}')
        self.database.commit()
    
    def get_last_updated(self):
        '''Returns the timestamp that realtime data was last updated'''
        return self.last_updated
    
    def validate(self, context: Context):
        '''Checks that the realtime data for the given context aligns with the current GTFS for that system'''
        if not context.realtime_enabled:
            return True
        for position in self.position_repository.find_all(context):
            trip_id = position.trip_id
            if not trip_id:
                continue
            if not position.trip:
                trip_id_sections = trip_id.split(':')
                if len(trip_id_sections) == 3:
                    block_id = trip_id_sections[2]
                    if not context.system.get_block(block_id):
                        return False
                else:
                    return False
        return True
