
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
        block = position.trip.block
        hour = datetime.now().hour
        today = datetime.today()
        date = today if hour >= 5 else today - timedelta(days=1)
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
                        'rowid': last_record.id
                    })
                continue
        
        database.insert('records', {
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
    database.commit()

def get_last_seen(system):
    filters = {
        'rn': 1
    }
    if system is not None:
        filters['system_id'] = system.id
    records_data = database.select('''
        (
            SELECT rowid, bus_number, date, system_id, block_id, routes, start_time, end_time,
                ROW_NUMBER() OVER(PARTITION BY bus_number ORDER BY date DESC, start_time DESC) AS rn
            FROM records
        )
        ''',
        columns=['rowid', 'bus_number', 'date', 'system_id', 'block_id', 'routes', 'start_time', 'end_time', 'first_seen', 'last_seen'],
        filters=filters,
        order_by='bus_number')
    records = []
    for data in records_data:
        record_id = data['rowid']
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
        columns=['rowid', 'date', 'system_id', 'block_id', 'routes', 'start_time', 'end_time', 'first_seen', 'last_seen'],
        filters={
            'bus_number': bus.number
        },
        order_by='date DESC, start_time DESC',
        limit=limit)
    records = []
    for data in records_data:
        record_id = data['rowid']
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
        columns=['rowid', 'bus_number', 'date', 'system_id', 'routes', 'start_time', 'end_time', 'first_seen', 'last_seen'],
        filters={
            'block_id': block.id
        },
        order_by='date DESC, start_time DESC',
        limit=limit)
    records = []
    for data in records_data:
        record_id = data['rowid']
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
