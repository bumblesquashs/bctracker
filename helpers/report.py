
from models.report import Report

import database

def create(bus, date, system, record_id):
    database.insert('reports', {
        'bus_number': bus.number,
        'first_seen_date': date.format_db(),
        'first_seen_system_id': system.id,
        'first_record_id': record_id,
        'last_seen_date': date.format_db(),
        'last_seen_system_id': system.id,
        'last_record_id': record_id
    })

def find(bus_number):
    reports = find_all(bus_number=bus_number, limit=1)
    if len(reports) == 1:
        return reports[0]
    return None

def find_all(system_id=None, bus_number=None, limit=None):
    rows = database.select('reports',
        columns={
            'reports.bus_number': 'report_number',
            'reports.first_seen_date': 'report_first_seen_date',
            'reports.first_seen_system_id': 'report_first_seen_system_id',
            'reports.last_seen_date': 'report_last_seen_date',
            'reports.last_seen_system_id': 'report_last_seen_system_id',
            'first_record.record_id': 'report_first_record_id',
            'first_record.bus_number': 'report_first_record_bus_number',
            'first_record.date': 'report_first_record_date',
            'first_record.system_id': 'report_first_record_system_id',
            'first_record.block_id': 'report_first_record_block_id',
            'first_record.routes': 'report_first_record_routes',
            'first_record.start_time': 'report_first_record_start_time',
            'first_record.end_time': 'report_first_record_end_time',
            'first_record.first_seen': 'report_first_record_first_seen',
            'first_record.last_seen': 'report_first_record_last_seen',
            'last_record.record_id': 'report_last_record_id',
            'last_record.bus_number': 'report_last_record_bus_number',
            'last_record.date': 'report_last_record_date',
            'last_record.system_id': 'report_last_record_system_id',
            'last_record.block_id': 'report_last_record_block_id',
            'last_record.routes': 'report_last_record_routes',
            'last_record.start_time': 'report_last_record_start_time',
            'last_record.end_time': 'report_last_record_end_time',
            'last_record.first_seen': 'report_last_record_first_seen',
            'last_record.last_seen': 'report_last_record_last_seen'
        },
        join_type='LEFT',
        joins={
            'records first_record': {
                'first_record.record_id': 'reports.first_record_id'
            },
            'records last_record': {
                'last_record.record_id': 'reports.last_record_id'
            }
        },
        filters={
            'reports.bus_number': bus_number,
            'last_record.system_id': system_id
        },
        limit=limit)
    return [Report.from_db(row) for row in rows]

def update(report, date, system, record_id):
    values = {
        'last_seen_date': date.format_db(),
        'last_seen_system_id': system.id
    }
    if record_id is not None:
        if report.first_record is None:
            values['first_record_id'] = record_id
        values['last_record_id'] = record_id
    database.update('reports', values, {
        'bus_number': report.bus.number
    })
