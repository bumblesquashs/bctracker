
from dataclasses import dataclass

from database import Database

from models.allocation import Allocation
from models.context import Context
from models.date import Date
from models.stop import Stop

@dataclass(slots=True)
class AllocationRepository:
    
    database: Database
    
    def create(self, context: Context, vehicle_id: str, date: Date, lat: float | None, lon: float | None, stop: Stop | None, active: bool = True):
        return self.database.insert(
            table='allocation',
            values={
                'agency_id': context.agency_id,
                'vehicle_id': vehicle_id,
                'system_id': context.system_id,
                'first_seen': date.format_db(),
                'last_seen': date.format_db(),
                'active': 1 if active else 0,
                'last_lat': lat,
                'last_lon': lon,
                'last_stop_id': stop.id if stop else None,
                'last_stop_number': stop.number if stop else None,
                'last_stop_name': stop.name if stop else None
            }
        )
    
    def find_active(self, context: Context, vehicle_id: str) -> Allocation | None:
        allocations = self.find_all(context, vehicle_id, True, 1)
        try:
            return allocations[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context, vehicle_id: str | None = None, active: bool | None = None, limit: int | None = None) -> list[Allocation]:
        filters = {
            'allocation.agency_id': context.agency_id,
            'allocation.vehicle_id': vehicle_id,
            'allocation.system_id': context.system_id,
        }
        if active is not None:
            filters['allocation.active'] = 1 if active else 0
        return self.database.select(
            table='allocation',
            columns={
                'allocation.allocation_id': 'id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'allocation.first_seen': 'first_seen',
                'first_record.record_id': 'first_record_id',
                'first_record.date': 'first_record_date',
                'first_record.block_id': 'first_record_block_id',
                'first_record.route_numbers': 'first_record_route_numbers',
                'first_record.start_time': 'first_record_start_time',
                'first_record.end_time': 'first_record_end_time',
                'first_record.first_seen': 'first_record_first_seen',
                'first_record.last_seen': 'first_record_last_seen',
                'allocation.last_seen': 'last_seen',
                'last_record.record_id': 'last_record_id',
                'last_record.date': 'last_record_date',
                'last_record.block_id': 'last_record_block_id',
                'last_record.route_numbers': 'last_record_route_numbers',
                'last_record.start_time': 'last_record_start_time',
                'last_record.end_time': 'last_record_end_time',
                'last_record.first_seen': 'last_record_first_seen',
                'last_record.last_seen': 'last_record_last_seen',
                'allocation.active': 'active',
                'allocation.last_lat': 'last_lat',
                'allocation.last_lon': 'last_lon',
                'allocation.last_stop_id': 'last_stop_id',
                'allocation.last_stop_number': 'last_stop_number',
                'allocation.last_stop_name': 'last_stop_name'
            },
            filters=filters,
            join_type='LEFT',
            joins={
                'allocation_record': {
                    'allocation_record.allocation_id': 'allocation.allocation_id'
                },
                'record first_record': {
                    'first_record.record_id': 'allocation_record.first_record_id'
                },
                'record last_record': {
                    'last_record.record_id': 'allocation_record.last_record_id'
                }
            },
            limit=limit,
            initializer=Allocation.from_db
        )
    
    def find_all_last_seen(self, context: Context, active: bool | None) -> list[Allocation]:
        filters = {
            'allocation.agency_id': context.agency_id,
            'allocation.system_id': context.system_id
        }
        if active is not None:
            filters['allocation.active'] = 1 if active else 0
        return self.database.select(
            table='allocation',
            columns={
                'allocation.allocation_id': 'id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'allocation.first_seen': 'first_seen',
                'first_record.record_id': 'first_record_id',
                'first_record.date': 'first_record_date',
                'first_record.block_id': 'first_record_block_id',
                'first_record.route_numbers': 'first_record_route_numbers',
                'first_record.start_time': 'first_record_start_time',
                'first_record.end_time': 'first_record_end_time',
                'first_record.first_seen': 'first_record_first_seen',
                'first_record.last_seen': 'first_record_last_seen',
                'allocation.last_seen': 'last_seen',
                'last_record.record_id': 'last_record_id',
                'last_record.date': 'last_record_date',
                'last_record.block_id': 'last_record_block_id',
                'last_record.route_numbers': 'last_record_route_numbers',
                'last_record.start_time': 'last_record_start_time',
                'last_record.end_time': 'last_record_end_time',
                'last_record.first_seen': 'last_record_first_seen',
                'last_record.last_seen': 'last_record_last_seen',
                'allocation.active': 'active',
                'allocation.last_lat': 'last_lat',
                'allocation.last_lon': 'last_lon',
                'allocation.last_stop_id': 'last_stop_id',
                'allocation.last_stop_number': 'last_stop_number',
                'allocation.last_stop_name': 'last_stop_name',
                'MAX(allocation.last_seen)': 'max_last_seen'
            },
            filters=filters,
            join_type='LEFT',
            joins={
                'allocation_record': {
                    'allocation_record.allocation_id': 'allocation.allocation_id'
                },
                'record first_record': {
                    'first_record.record_id': 'allocation_record.first_record_id'
                },
                'record last_record': {
                    'last_record.record_id': 'allocation_record.last_record_id'
                }
            },
            group_by=[
                'allocation.agency_id',
                'allocation.vehicle_id'
            ],
            initializer=Allocation.from_db
        )
    
    def find_all_first_seen(self, context: Context, active: bool | None) -> list[Allocation]:
        filters = {
            'allocation.agency_id': context.agency_id,
            'allocation.system_id': context.system_id
        }
        if active is not None:
            filters['allocation.active'] = 1 if active else 0
        return self.database.select(
            table='allocation',
            columns={
                'allocation.allocation_id': 'id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'allocation.first_seen': 'first_seen',
                'first_record.record_id': 'first_record_id',
                'first_record.date': 'first_record_date',
                'first_record.block_id': 'first_record_block_id',
                'first_record.route_numbers': 'first_record_route_numbers',
                'first_record.start_time': 'first_record_start_time',
                'first_record.end_time': 'first_record_end_time',
                'first_record.first_seen': 'first_record_first_seen',
                'first_record.last_seen': 'first_record_last_seen',
                'allocation.last_seen': 'last_seen',
                'last_record.record_id': 'last_record_id',
                'last_record.date': 'last_record_date',
                'last_record.block_id': 'last_record_block_id',
                'last_record.route_numbers': 'last_record_route_numbers',
                'last_record.start_time': 'last_record_start_time',
                'last_record.end_time': 'last_record_end_time',
                'last_record.first_seen': 'last_record_first_seen',
                'last_record.last_seen': 'last_record_last_seen',
                'allocation.active': 'active',
                'allocation.last_lat': 'last_lat',
                'allocation.last_lon': 'last_lon',
                'allocation.last_stop_id': 'last_stop_id',
                'allocation.last_stop_number': 'last_stop_number',
                'allocation.last_stop_name': 'last_stop_name',
                'MIN(allocation.first_seen)': 'min_first_seen'
            },
            filters=filters,
            join_type='LEFT',
            joins={
                'allocation_record': {
                    'allocation_record.allocation_id': 'allocation.allocation_id'
                },
                'record first_record': {
                    'first_record.record_id': 'allocation_record.first_record_id'
                },
                'record last_record': {
                    'last_record.record_id': 'allocation_record.last_record_id'
                }
            },
            group_by=[
                'allocation.agency_id',
                'allocation.vehicle_id'
            ],
            initializer=Allocation.from_db
        )
    
    def find_vehicle_ids(self, context: Context) -> set[str]:
        '''Returns all vehicle IDs that have been seen'''
        vehicle_ids = self.database.select(
            table='allocation',
            columns=[
                'vehicle_id'
            ],
            filters={
                'agency_id': context.agency_id,
                'system_id': context.system_id
            },
            initializer=lambda r: r['vehicle_id']
        )
        return set(vehicle_ids)
    
    def set_inactive(self, allocation_id: int):
        self.database.update(
            table='allocation',
            values={
                'active': 0
            },
            filters={
                'allocation_id': allocation_id
            }
        )
    
    def set_last_seen(self, allocation_id: int, date: Date, lat: float | None, lon: float | None, stop: Stop | None):
        self.database.update(
            table='allocation',
            values={
                'last_seen': date.format_db(),
                'last_lat': lat,
                'last_lon': lon,
                'last_stop_id': stop.id if stop else None,
                'last_stop_number': stop.number if stop else None,
                'last_stop_name': stop.name if stop else None
            },
            filters={
                'allocation_id': allocation_id
            }
        )
    
    def set_first_record(self, allocation_id: int, record_id: int):
        self.database.upsert(
            table='allocation_record',
            conflict_column='allocation_id',
            insert_values={
                'allocation_id': allocation_id,
                'first_record_id': record_id
            },
            update_values={
                'first_record_id': record_id
            }
        )
    
    def set_last_record(self, allocation_id: int, record_id: int):
        self.database.upsert(
            table='allocation_record',
            conflict_column='allocation_id',
            insert_values={
                'allocation_id': allocation_id,
                'last_record_id': record_id
            },
            update_values={
                'last_record_id': record_id
            }
        )
