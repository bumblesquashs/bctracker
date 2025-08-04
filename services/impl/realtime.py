
from os import path, rename, remove
from dataclasses import dataclass
from datetime import datetime

import requests

import protobuf.data.gtfs_realtime_pb2 as protobuf

from database import Database
from settings import Settings

from models.context import Context
from models.date import Date
from models.time import Time
from models.timestamp import Timestamp

import repositories

@dataclass(slots=True)
class RealtimeService:
    
    database: Database
    settings: Settings
    last_updated: Date | None = None
    
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
        repositories.position.delete_all(context)
        for index, entity in enumerate(data.entity):
            vehicle = entity.vehicle
            try:
                vehicle_id = vehicle.vehicle.id
                vehicle_name_length = context.vehicle_name_length
                if vehicle_name_length and len(vehicle_id) > vehicle_name_length:
                    vehicle_id = vehicle_id[-vehicle_name_length:]
            except:
                vehicle_id = str(-(index + 1))
            repositories.position.create(context, vehicle_id, vehicle)
        self.last_updated = Timestamp.now(accurate_seconds=False)
        context.system.last_updated = Timestamp.now(context.timezone, context.accurate_seconds)
    
    def update_records(self):
        '''Updates records in the database based on the current positions in the database'''
        for position in repositories.position.find_all():
            try:
                context = position.context
                bus = position.bus
                if not bus.is_known:
                    continue
                date = Date.today(context.timezone)
                time = Time.now(context.timezone)
                
                allocation = repositories.allocation.find_active(context, bus.id)
                if allocation:
                    if allocation.context == context:
                        repositories.allocation.set_last_seen(allocation.id, date, position.lat, position.lon, position.stop)
                        allocation_id = allocation.id
                        first_record = allocation.first_record
                        last_record = allocation.last_record
                    else:
                        repositories.allocation.set_inactive(allocation.id)
                        repositories.assignment.delete_all(allocation_id=allocation.id)
                        allocation_id = repositories.allocation.create(context, bus.id, date, position.lat, position.lon, position.stop)
                        repositories.transfer.create(date, allocation.id, allocation_id)
                        first_record = None
                        last_record = None
                else:
                    allocation_id = repositories.allocation.create(context, bus.id, date, position.lat, position.lon, position.stop)
                    first_record = None
                    last_record = None
                
                if position.trip and position.block_id and position.block:
                    assignment = repositories.assignment.find(position.block_id, allocation_id, date)
                    if not assignment or assignment.allocation_id != allocation_id:
                        repositories.assignment.delete_all(block_id=position.block_id)
                        repositories.assignment.delete_all(allocation_id=allocation_id)
                        repositories.assignment.create(position.block_id, allocation_id, date)
                    
                    if last_record and last_record.date == date and last_record.block_id == position.block_id:
                        record_id = last_record.id
                        repositories.record.update(last_record.id, time)
                        trip_ids = repositories.record.find_trip_ids(last_record.id)
                        if position.trip_id not in trip_ids:
                            repositories.record.create_trip(last_record.id, position.trip_id)
                    else:
                        record_id = repositories.record.create(allocation_id, date, position.block, time, position.trip_id)
                    
                    if not first_record:
                        repositories.allocation.set_first_record(allocation_id, record_id)
                    if not last_record or last_record.id != record_id:
                        repositories.allocation.set_last_record(allocation_id, record_id)
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
        for position in repositories.position.find_all(context):
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
