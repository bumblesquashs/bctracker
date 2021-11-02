
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
        block = position.trip.block
        hour = datetime.now().hour
        today = datetime.today()
        date = today if hour >= 5 else today - timedelta(days=1)
        
        records = get_bus_records(bus, limit=1)
        if len(records) > 0:
            last_record = records[0]
            if last_record.date.date() == date.date() and last_record.block_id == block.id:
                continue
        
        database.insert('records', {
            'bus_number': bus.number,
            'date': date.strftime('%Y-%m-%d'),
            'system_id': position.system.id,
            'block_id': block.id,
            'routes': block.get_routes_string(Sheet.CURRENT),
            'start_time': block.get_start_time(Sheet.CURRENT).full_string,
            'end_time': block.get_end_time(Sheet.CURRENT).full_string
        })
    database.commit()

def get_last_seen(system):
    filters = ['''
        rowid = (
            SELECT rowid
            FROM records r2
            WHERE r2.bus_number = r1.bus_number
            ORDER BY date DESC, start_time DESC
            LIMIT 1
        )
    ''']
    args = None
    if system is not None:
        filters.append('system_id = ?')
        args = [system.id]
    records_data = database.select('records r1',
        columns=['bus_number', 'date', 'system_id', 'block_id', 'routes', 'start_time', 'end_time'],
        filters=filters,
        order_by='bus_number',
        args=args)
    records = []
    for data in records_data:
        bus = Bus(data['bus_number'])
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        system_id = data['system_id']
        block_id = data['block_id']
        routes = data['routes']
        start_time = Time(data['start_time'])
        end_time = Time(data['end_time'])
        
        records.append(Record(bus, date, system_id, block_id, routes, start_time, end_time))
    return records

def get_bus_records(bus, limit=None):
    records_data = database.select('records', 
        columns=['date', 'system_id', 'block_id', 'routes', 'start_time', 'end_time'],
        filters={
            'bus_number': bus.number
        },
        order_by='date DESC, start_time DESC',
        limit=limit)
    records = []
    for data in records_data:
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        system_id = data['system_id']
        block_id = data['block_id']
        routes = data['routes']
        start_time = Time(data['start_time'])
        end_time = Time(data['end_time'])
        
        records.append(Record(bus, date, system_id, block_id, routes, start_time, end_time))
    return records
