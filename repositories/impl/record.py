
from dataclasses import dataclass
from datetime import timedelta

from database import Database

from models.block import Block
from models.bus import Bus
from models.context import Context
from models.date import Date
from models.record import Record
from models.time import Time

@dataclass(slots=True)
class RecordRepository:
    
    database: Database
    
    def create(self, allocation_id: int, date: Date, block: Block, time: Time, trip_id: str):
        '''Inserts a new record into the database'''
        record_id = self.database.insert(
            table='record',
            values={
                'allocation_id': allocation_id,
                'date': date.format_db(),
                'block_id': block.id,
                'routes': block.get_routes_string(date=date),
                'start_time': block.get_start_time(date=date).format_db(),
                'end_time': block.get_end_time(date=date).format_db(),
                'first_seen': time.format_db(),
                'last_seen': time.format_db()
            }
        )
        self.create_trip(record_id, trip_id)
        return record_id
    
    def create_trip(self, record_id: int, trip_id: str):
        '''Inserts a new trip record into the database'''
        self.database.insert(
            table='trip_record',
            values={
                'record_id': record_id,
                'trip_id': trip_id
            }
        )
    
    def update(self, record_id: int, time: Time):
        '''Updates a record in the database'''
        self.database.update(
            table='record',
            values={
                'last_seen': time.format_db()
            },
            filters={
                'record_id': record_id
            }
        )
    
    def find_all(self, context: Context = Context(), bus=None, block=None, trip=None, limit=None, page=None) -> list[Record]:
        '''Returns all records that match the given context, bus, block, and trip'''
        vehicle_id = getattr(bus, 'number', bus)
        block_id = getattr(block, 'id', block)
        trip_id = getattr(trip, 'id', trip)
        joins = {
            'allocation': {
                'allocation.allocation_id': 'record.allocation_id'
            }
        }
        filters = {
            'allocation.agency_id': context.agency_id,
            'allocation.vehicle_id': vehicle_id,
            'allocation.system_id': context.system_id,
            'record.block_id': block_id
        }
        if trip_id:
            joins['trip_record'] = {
                'trip_record.record_id': 'record.record_id'
            }
            filters['trip_record.trip_id'] = trip_id
        return self.database.select(
            table='record', 
            columns={
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id',
                'allocation.system_id': 'system_id',
                'record.record_id': 'id',
                'record.allocation_id': 'allocation_id',
                'record.date': 'date',
                'record.block_id': 'block_id',
                'record.routes': 'routes',
                'record.start_time': 'start_time',
                'record.end_time': 'end_time',
                'record.first_seen': 'first_seen',
                'record.last_seen': 'last_seen'
            },
            joins=joins,
            filters=filters,
            order_by={
                'record.date': 'DESC',
                'record.record_id': 'DESC'
            },
            limit=limit,
            page=page,
            initializer=Record.from_db
        )
    
    def find_trip_ids(self, record_id: int) -> list[str]:
        '''Returns all trip IDs associated with the given record'''
        return self.database.select('trip_record', columns=['trip_id'], filters={'record_id': record_id}, initializer=lambda r: r['trip_id'])
    
    def find_recorded_today(self, context: Context, trips) -> dict[str: Bus]:
        '''Returns all bus numbers matching the given context and trips that were recorded on the current date'''
        trip_ids = [getattr(t, 'id', t) for t in trips]
        date = Date.today(context.timezone)
        rows = self.database.select(
            table='trip_record',
            columns={
                'trip_record.trip_id': 'trip_id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id'
            },
            joins={
                'record': {
                    'record.record_id': 'trip_record.record_id'
                },
                'allocation': {
                    'allocation.allocation_id': 'record.allocation_id'
                }
            },
            filters={
                'allocation.agency_id': context.agency_id,
                'allocation.system_id': context.system_id,
                'record.date': date.format_db(),
                'trip_record.trip_id': trip_ids
            },
            order_by='record.last_seen ASC'
        )
        return {row['trip_id']: context.find_bus(row['vehicle_id']) for row in rows}
    
    def find_recorded_today_by_block(self, context: Context) -> dict[str, Bus]:
        '''Returns all bus numbers matching the given context that werer ecorded on the current date'''
        date = Date.today(context.timezone)
        rows = self.database.select(
            table='record',
            columns={
                'record.block_id': 'block_id',
                'allocation.agency_id': 'agency_id',
                'allocation.vehicle_id': 'vehicle_id'
            },
            filters={
                'allocation.agency_id': context.agency_id,
                'allocation.system_id': context.system_id,
                'record.date': date.format_db()
            },
            joins={
                'allocation': {
                    'allocation.allocation_id': 'record.allocation_id'
                }
            },
            order_by='record.last_seen ASC'
        )
        return {row['block_id']: context.find_bus(row['vehicle_id']) for row in rows}
    
    def count(self, context: Context = Context(), bus=None, block=None, trip=None) -> int:
        '''Returns the number of records for the given system, bus, block, and trip'''
        vehicle_id = getattr(bus, 'number', bus)
        block_id = getattr(block, 'id', block)
        trip_id = getattr(trip, 'id', trip)
        joins = {
            'allocation': {
                'allocation.allocation_id': 'record.allocation_id'
            }
        }
        filters = {
            'allocation.agency_id': context.agency_id,
            'allocation.vehicle_id': vehicle_id,
            'allocation.system_id': context.system_id,
            'record.block_id': block_id
        }
        if trip_id:
            joins['trip_record'] = {
                'trip_record.record_id': 'record.record_id'
            }
            filters['trip_record.trip_id'] = trip_id
        counts = self.database.select(
            table='record', 
            columns={
                'COUNT(record.record_id)': 'count'
            },
            joins=joins,
            filters=filters,
            initializer=lambda r: r['count']
        )
        try:
            return counts[0]
        except IndexError:
            return 0
    
    def delete_stale_trip_records(self):
        '''Removes all old and unused trip records'''
        date = Date.today() - timedelta(days=90)
        self.database.execute('''
            DELETE FROM trip_record
            WHERE trip_record_id IN (
                SELECT trip_record_id
                FROM trip_record
                JOIN record ON record.record_id = trip_record.record_id
                JOIN allocation ON allocation.allocation_id = record.allocation_id
                WHERE record.date < ?
                AND NOT EXISTS (
                    SELECT 1
                    FROM trip
                    WHERE trip.trip_id = trip_record.trip_id
                        AND trip.system_id = allocation.system_id
                )
            )
        ''', [date.format_db()])
