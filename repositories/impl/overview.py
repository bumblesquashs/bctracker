
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.overview import Overview

@dataclass(slots=True)
class OverviewRepository:
    
    database: Database
    
    def create(self, context: Context, bus, date, record):
        '''Inserts a new overview into the database'''
        bus_number = getattr(bus, 'number', bus)
        record_id = getattr(record, 'id', record)
        self.database.insert('overview', {
            'agency_id': context.agency_id,
            'bus_number': bus_number,
            'first_seen_date': date.format_db(),
            'first_seen_system_id': context.system_id,
            'first_record_id': record_id,
            'last_seen_date': date.format_db(),
            'last_seen_system_id': context.system_id,
            'last_record_id': record_id
        })
    
    def find(self, bus) -> Overview | None:
        '''Returns the overview of the given bus'''
        overviews = self.find_all(bus=bus, limit=1)
        try:
            return overviews[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context = Context(), last_seen_context: Context = Context(), bus=None, limit=None) -> list[Overview]:
        '''Returns all overviews that match the given context and bus'''
        bus_number = getattr(bus, 'number', bus)
        return self.database.select('overview',
            columns={
                'overview.agency_id': 'agency_id',
                'overview.bus_number': 'bus_number',
                'overview.first_seen_date': 'first_seen_date',
                'overview.first_seen_system_id': 'first_seen_system_id',
                'overview.last_seen_date': 'last_seen_date',
                'overview.last_seen_system_id': 'last_seen_system_id',
                'first_record.record_id': 'first_record_id',
                'first_record.agency_id': 'first_record_agency_id',
                'first_record.bus_number': 'first_record_bus_number',
                'first_record.date': 'first_record_date',
                'first_record.system_id': 'first_record_system_id',
                'first_record.block_id': 'first_record_block_id',
                'first_record.routes': 'first_record_routes',
                'first_record.start_time': 'first_record_start_time',
                'first_record.end_time': 'first_record_end_time',
                'first_record.first_seen': 'first_record_first_seen',
                'first_record.last_seen': 'first_record_last_seen',
                'last_record.record_id': 'last_record_id',
                'last_record.agency_id': 'last_record_agency_id',
                'last_record.bus_number': 'last_record_bus_number',
                'last_record.date': 'last_record_date',
                'last_record.system_id': 'last_record_system_id',
                'last_record.block_id': 'last_record_block_id',
                'last_record.routes': 'last_record_routes',
                'last_record.start_time': 'last_record_start_time',
                'last_record.end_time': 'last_record_end_time',
                'last_record.first_seen': 'last_record_first_seen',
                'last_record.last_seen': 'last_record_last_seen'
            },
            join_type='LEFT',
            joins={
                'record first_record': {
                    'first_record.record_id': 'overview.first_record_id'
                },
                'record last_record': {
                    'last_record.record_id': 'overview.last_record_id'
                }
            },
            filters={
                'overview.agency_id': context.agency_id,
                'overview.bus_number': bus_number,
                'last_record.system_id': context.system_id,
                'overview.last_seen_system_id': last_seen_context.system_id
            },
            limit=limit,
            initializer=Overview.from_db
        )
    
    def find_bus_numbers(self, context: Context) -> list[str]:
        '''Returns all bus numbers that have been seen'''
        joins = {}
        filters = {}
        if context.system:
            joins['record last_record'] = {
                'last_record.record_id': 'overview.last_record_id'
            }
            filters['last_record.system_id'] = context.system_id
        return self.database.select('overview',
            columns={
                'overview.bus_number': 'bus_number'
            },
            join_type='LEFT',
            joins=joins,
            filters=filters,
            initializer=lambda r: r['bus_number']
        )
    
    def update(self, context: Context, overview, date, record):
        '''Updates an overview in the database'''
        record_id = getattr(record, 'id', record)
        values = {
            'last_seen_date': date.format_db(),
            'last_seen_system_id': context.system_id
        }
        if record_id:
            if not overview.first_record:
                values['first_record_id'] = record_id
            values['last_record_id'] = record_id
        self.database.update('overview', values, {
            'agency_id': overview.bus.agency.id,
            'bus_number': overview.bus.number
        })
