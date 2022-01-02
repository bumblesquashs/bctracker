
from datetime import datetime, timedelta

from models.bus import Bus
from models.record import Record
from models.service import Sheet
from models.time import Time

import database

def update(positions):
    for position in positions:
        if not position.active or position.trip is None:
            continue
        bus = position.bus
        if bus.is_unknown:
            continue
        trip = position.trip
        block = trip.block
        hour = datetime.now().hour
        today = datetime.today()
        date = today if hour >= 4 else today - timedelta(days=1)
        now = datetime.now().strftime('%H:%M')
        
        records = get_bus_records(bus, limit=1)
        if len(records) > 0:
            last_record = records[0]
            if last_record.date.date() == date.date() and last_record.block_id == block.id:
                database.update('records',
                    values={
                        'last_seen': now
                    },
                    filters={
                        'record_id': last_record.id
                    })
                trip_ids = get_trip_ids(last_record)
                if trip.id not in trip_ids:
                    database.insert('trip_records', {
                        'record_id': last_record.id,
                        'trip_id': trip.id
                    })
                continue
        
        record_id = database.insert('records', {
            'bus_number': bus.number,
            'date': date.strftime('%Y-%m-%d'),
            'system_id': position.system.id,
            'block_id': block.id,
            'routes': block.get_routes_string(Sheet.CURRENT),
            'start_time': block.get_start_time(Sheet.CURRENT).full_string,
            'end_time': block.get_end_time(Sheet.CURRENT).full_string,
            'first_seen': now,
            'last_seen': now
        })
        database.insert('trip_records', {
            'record_id': record_id,
            'trip_id': trip.id
        })
    database.commit()

def get_last_seen(system):
    filters = {
        'rn': 1
    }
    if system is not None:
        filters['system_id'] = system.id
    records_data = database.select('''
        (
            SELECT record_id, bus_number, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen,
                ROW_NUMBER() OVER(PARTITION BY bus_number ORDER BY date DESC, start_time DESC) AS rn
            FROM records
        )
        ''',
        columns=['record_id', 'bus_number', 'date', 'system_id', 'block_id', 'routes', 'start_time', 'end_time', 'first_seen', 'last_seen'],
        filters=filters,
        order_by='bus_number')
    records = []
    for data in records_data:
        record_id = data['record_id']
        bus = Bus(data['bus_number'])
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        system_id = data['system_id']
        block_id = data['block_id']
        routes = data['routes']
        start_time = Time(data['start_time'])
        end_time = Time(data['end_time'])
        first_seen = Time(data['first_seen'])
        last_seen = Time(data['last_seen'])
        
        records.append(Record(record_id, bus, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen))
    return records

def get_bus_records(bus, limit=None):
    records_data = database.select('records', 
        columns=['record_id', 'date', 'system_id', 'block_id', 'routes', 'start_time', 'end_time', 'first_seen', 'last_seen'],
        filters={
            'bus_number': bus.number
        },
        order_by='date DESC, record_id DESC',
        limit=limit)
    records = []
    for data in records_data:
        record_id = data['record_id']
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        system_id = data['system_id']
        block_id = data['block_id']
        routes = data['routes']
        start_time = Time(data['start_time'])
        end_time = Time(data['end_time'])
        first_seen = Time(data['first_seen'])
        last_seen = Time(data['last_seen'])
        
        records.append(Record(record_id, bus, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen))
    return records

def get_block_records(block, limit=None):
    records_data = database.select('records', 
        columns=['record_id', 'bus_number', 'date', 'system_id', 'routes', 'start_time', 'end_time', 'first_seen', 'last_seen'],
        filters={
            'block_id': block.id,
            'system_id': block.system.id
        },
        order_by='date DESC, record_id DESC',
        limit=limit)
    records = []
    for data in records_data:
        record_id = data['record_id']
        bus = Bus(data['bus_number'])
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        system_id = data['system_id']
        routes = data['routes']
        start_time = Time(data['start_time'])
        end_time = Time(data['end_time'])
        first_seen = Time(data['first_seen'])
        last_seen = Time(data['last_seen'])
        
        records.append(Record(record_id, bus, date, system_id, block.id, routes, start_time, end_time, first_seen, last_seen))
    return records

def get_trip_ids(record):
    trip_records_data = database.select('trip_records',
        columns=['trip_id'],
        filters={
            'record_id': record.id
        })
    trip_ids = set()
    for data in trip_records_data:
        trip_ids.add(data['trip_id'])
    return trip_ids

def get_trip_records(trip, limit=None):
    records_data = database.select('trip_records tr',
        columns=['tr.record_id', 'r.bus_number', 'r.date', 'r.system_id', 'r.block_id', 'r.routes', 'r.start_time', 'r.end_time', 'r.first_seen', 'r.last_seen'],
        joins={
            'records r': 'r.record_id = tr.record_id'
        },
        filters={
            'tr.trip_id': trip.id,
            'r.system_id': trip.system.id
        },
        order_by='date DESC, tr.record_id DESC',
        limit=limit)
    records = []
    for data in records_data:
        record_id = data['tr.record_id']
        bus = Bus(data['r.bus_number'])
        date = datetime.strptime(data['r.date'], '%Y-%m-%d')
        system_id = data['r.system_id']
        block_id = data['r.block_id']
        routes = data['r.routes']
        start_time = Time(data['r.start_time'])
        end_time = Time(data['r.end_time'])
        first_seen = Time(data['r.first_seen'])
        last_seen = Time(data['r.last_seen'])
        
        records.append(Record(record_id, bus, date, system_id, block_id, routes, start_time, end_time, first_seen, last_seen))
    return records

def recorded_buses(system):
    filters = None
    if system is not None:
        filters = {
            'system_id': system.id
        }
    records_data = database.select('records', columns=['DISTINCT bus_number'], filters=filters)
    buses = []
    for data in records_data:
        buses.append(Bus(data['DISTINCT bus_number']))
    return buses
