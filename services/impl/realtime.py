
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
                bus_number = int(vehicle_id)
            except:
                bus_number = -(index + 1)
            repositories.position.create(context, bus_number, vehicle)
        self.last_updated = Timestamp.now(accurate_seconds=False)
        context.system.last_updated = Timestamp.now(context.timezone, context.accurate_seconds)
    
    def update_records(self):
        '''Updates records in the database based on the current positions in the database'''
        for position in repositories.position.find_all():
            try:
                context = position.context
                bus = position.bus
                if bus.number < 0:
                    continue
                date = Date.today(context.timezone)
                time = Time.now(context.timezone)
                overview = repositories.overview.find(bus.number)
                trip = position.trip
                if trip:
                    block = trip.block
                    assignment = repositories.assignment.find(context, block)
                    if not assignment or assignment.bus_number != bus.number:
                        repositories.assignment.delete_all(context, block=block)
                        repositories.assignment.delete_all(Context(), bus=bus)
                        repositories.assignment.create(context, block, bus, date)
                    if overview and overview.last_record:
                        last_record = overview.last_record
                        if last_record.date == date and last_record.block_id == block.id:
                            repositories.record.update(last_record, time)
                            trip_ids = repositories.record.find_trip_ids(last_record)
                            if trip.id not in trip_ids:
                                repositories.record.create_trip(last_record, trip)
                            continue
                    record_id = repositories.record.create(context, bus, date, block, time, trip)
                else:
                    record_id = None
                if overview:
                    repositories.overview.update(context, overview, date, record_id)
                    if overview.last_seen_context != context:
                        repositories.transfer.create(bus, date, overview.last_seen_context, context)
                else:
                    repositories.overview.create(context, bus, date, record_id)
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
