
from os import path, rename, remove
from dataclasses import dataclass
from datetime import datetime

import requests

import protobuf.data.gtfs_realtime_pb2 as protobuf

from database import Database
from settings import Settings

from models.block import Block
from models.bus import Bus
from models.context import Context
from models.date import Date
from models.position import Position
from models.time import Time
from models.timestamp import Timestamp

import repositories

@dataclass(slots=True)
class RealtimeService:
    
    database: Database
    settings: Settings
    last_updated: Date | None = None
    
    def update(self, context: Context) -> bool:
        '''Downloads realtime data for the given context and stores it in the database'''
        if not context.realtime_enabled:
            return True
        data_path = f'data/realtime/{context.system_id}.bin'
        
        print(f'Updating realtime data for {context}')
        
        invalid_positions = 0
        total_positions = 0
        
        date = Date.today(context.timezone)
        time = Time.now(context.timezone)
        
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
        if data.entity:
            trips = {t.id: t for t in repositories.trip.find_all(context)}
            stops = {s.id: s for s in repositories.stop.find_all(context)}
            block_ids = repositories.trip.find_all_block_ids(context)
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
                bus = Bus.find(context, bus_number)
                position = repositories.position.create(context, bus, vehicle, trips, stops)
                self.update_record(position, date, time, trips)
                total_positions += 1
                if position.trip_id and position.trip_id not in trips:
                    trip_id_sections = position.trip_id.split(':')
                    if len(trip_id_sections) == 3:
                        block_id = trip_id_sections[2]
                        if block_id not in block_ids:
                            invalid_positions += 1
                    else:
                        invalid_positions += 1
        self.last_updated = Timestamp.now(accurate_seconds=False)
        context.system.last_updated = Timestamp.now(context.timezone, context.accurate_seconds)
        self.database.commit()
        if total_positions == 0:
            return True
        return invalid_positions <= total_positions / 4
    
    def update_record(self, position: Position, date, time, trips):
        bus = position.bus
        if bus.number < 0:
            return
        overview = repositories.overview.find(bus.number)
        if position.trip_id in trips:
            assignment = repositories.assignment.find(position.context, position.block_id)
            if not assignment or assignment.bus_number != bus.number:
                repositories.assignment.delete_all(position.context, block=position.block_id)
                repositories.assignment.delete_all(Context(), bus=bus)
                repositories.assignment.create(position.context, position.block_id, bus, date)
            if overview and overview.last_record:
                last_record = overview.last_record
                if last_record.date == date and last_record.block_id == position.block_id:
                    repositories.record.update(last_record, time)
                    recorded_trip_ids = repositories.record.find_trip_ids(last_record)
                    if position.trip_id not in recorded_trip_ids:
                        repositories.record.create_trip(last_record, position.trip_id)
                    return
            block_trips = [t for t in trips.values() if t.block_id == position.block_id]
            block = Block(position.context, position.block_id, block_trips)
            record_id = repositories.record.create(position.context, bus, date, block, time, position.trip_id)
        else:
            record_id = None
        if overview:
            repositories.overview.update(position.context, overview, date, record_id)
            if overview.last_seen_context != position.context:
                repositories.transfer.create(bus, date, overview.last_seen_context, position.context)
        else:
            repositories.overview.create(position.context, bus, date, record_id)
    
    def get_last_updated(self):
        '''Returns the timestamp that realtime data was last updated'''
        return self.last_updated
