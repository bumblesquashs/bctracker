
from datetime import timedelta

from di import di
from database import Database

from models.bus import Bus
from models.context import Context
from models.date import Date
from models.record import Record

from repositories import AgencyRepository, RecordRepository

class SQLRecordRepository(RecordRepository):
    
    __slots__ = (
        'database',
        'agency_repository'
    )
    
    def __init__(self, database: Database, **kwargs):
        self.database = database
        self.agency_repository = kwargs.get('agency_repository') or di[AgencyRepository]
    
    def create(self, context: Context, bus, date, block, time, trip):
        '''Inserts a new record into the database'''
        bus_number = getattr(bus, 'number', bus)
        block_id = getattr(block, 'id', block)
        record_id = self.database.insert('record', {
            'bus_number': bus_number,
            'date': date.format_db(),
            'system_id': context.system_id,
            'block_id': block_id,
            'routes': block.get_routes_string(date=date),
            'start_time': block.get_start_time(date=date).format_db(),
            'end_time': block.get_end_time(date=date).format_db(),
            'first_seen': time.format_db(),
            'last_seen': time.format_db()
        })
        self.create_trip(record_id, trip)
        return record_id
    
    def create_trip(self, record, trip):
        '''Inserts a new trip record into the database'''
        record_id = getattr(record, 'id', record)
        trip_id = getattr(trip, 'id', trip)
        self.database.insert('trip_record', {
            'record_id': record_id,
            'trip_id': trip_id
        })
    
    def update(self, record, time):
        '''Updates a record in the database'''
        record_id = getattr(record, 'id', record)
        self.database.update('record',
            values={
                'last_seen': time.format_db()
            },
            filters={
                'record_id': record_id
            }
        )
    
    def find_all(self, context: Context, bus=None, block=None, trip=None, limit=None, page=None):
        '''Returns all records that match the given context, bus, block, and trip'''
        bus_number = getattr(bus, 'number', bus)
        block_id = getattr(block, 'id', block)
        trip_id = getattr(trip, 'id', trip)
        joins = {}
        filters = {
            'record.system_id': context.system_id,
            'record.bus_number': bus_number,
            'record.block_id': block_id
        }
        if trip_id:
            joins['trip_record'] = {
                'trip_record.record_id': 'record.record_id'
            }
            filters['trip_record.trip_id'] = trip_id
        return self.database.select('record', 
            columns={
                'record.record_id': 'record_id',
                'record.bus_number': 'record_bus_number',
                'record.date': 'record_date',
                'record.system_id': 'record_system_id',
                'record.block_id': 'record_block_id',
                'record.routes': 'record_routes',
                'record.start_time': 'record_start_time',
                'record.end_time': 'record_end_time',
                'record.first_seen': 'record_first_seen',
                'record.last_seen': 'record_last_seen'
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
    
    def find_trip_ids(self, record):
        '''Returns all trip IDs associated with the given record'''
        record_id = getattr(record, 'id', record)
        return self.database.select('trip_record', columns=['trip_id'], filters={'record_id': record_id}, initializer=lambda r: r['trip_id'])
    
    def find_recorded_today(self, context: Context, trips):
        '''Returns all bus numbers matching the given context and trips that were recorded on the current date'''
        trip_ids = [getattr(t, 'id', t) for t in trips]
        date = Date.today(context.timezone)
        rows = self.database.select('trip_record',
            columns={
                'trip_record.trip_id': 'trip_id',
                'record.bus_number': 'bus_number'
            },
            joins={
                'record': {
                    'record.record_id': 'trip_record.record_id'
                }
            },
            filters={
                'record.system_id': context.system_id,
                'record.date': date.format_db(),
                'trip_record.trip_id': trip_ids
            },
            order_by='record.last_seen ASC'
        )
        agency = self.agency_repository.find('bc-transit')
        return {row['trip_id']: Bus.find(agency, row['bus_number']) for row in rows}
    
    def find_recorded_today_by_block(self, context: Context):
        '''Returns all bus numbers matching the given context that werer ecorded on the current date'''
        date = Date.today(context.timezone)
        rows = self.database.select('record',
            columns={
                'record.block_id': 'block_id',
                'record.bus_number': 'bus_number'
            },
            filters={
                'record.system_id': context.system_id,
                'record.date': date.format_db()
            },
            order_by='record.last_seen ASC'
        )
        agency = self.agency_repository.find('bc-transit')
        return {row['block_id']: Bus.find(agency, row['bus_number']) for row in rows}
    
    def count(self, context: Context, bus=None, block=None, trip=None):
        '''Returns the number of records for the given system, bus, block, and trip'''
        bus_number = getattr(bus, 'number', bus)
        block_id = getattr(block, 'id', block)
        trip_id = getattr(trip, 'id', trip)
        joins = {}
        filters = {
            'record.system_id': context.system_id,
            'record.bus_number': bus_number,
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
                WHERE record.date < ?
                AND NOT EXISTS (
                    SELECT 1
                    FROM trip
                    WHERE trip.trip_id = trip_record.trip_id
                        AND trip.system_id = record.system_id
                )
            )
        ''', [date.format_db()])
