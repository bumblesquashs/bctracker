
from datetime import datetime, timedelta

from models.bus_history import BusHistory
from models.service import Sheet
from models.time import Time

import database

def update(buses):
    for bus in buses:
        position = bus.position
        if not position.active or position.trip is None:
            continue
        block = position.trip.block
        system = position.system
        hour = datetime.now().hour
        today = datetime.today()
        date = today if hour >= 5 else today - timedelta(days=1)
        
        history = load_history(bus, limit=1)
        if len(history) > 0:
            last_update = history[0]
            if last_update.date.date() == date.date() and last_update.block_id == block.id:
                continue
        
        database.insert('bus_history', {
            'bus_number': bus.number,
            'date': date.strftime('%Y-%m-%d'),
            'system_id': system.id,
            'feed_version': system.feed_version,
            'block_id': block.id,
            'routes': block.get_routes_string(Sheet.CURRENT),
            'start_time': block.get_start_time(Sheet.CURRENT).full_string,
            'end_time': block.get_end_time(Sheet.CURRENT).full_string
        })
    database.commit()

def get_last_seen():
    return []

def load_history(bus, limit=None):
    history_data = database.select('bus_history', 
        columns=['date', 'system_id', 'feed_version', 'block_id', 'routes', 'start_time', 'end_time'],
        filters={
            'bus_number': bus.number
        },
        order_by='date DESC, start_time DESC',
        limit=limit)
    history = []
    for data in history_data:
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        system_id = data['system_id']
        feed_version = data['feed_version']
        block_id = data['block_id']
        routes = data['routes']
        start_time = Time(data['start_time'])
        end_time = Time(data['end_time'])
        
        history.append(BusHistory(bus, date, system_id, feed_version, block_id, routes, start_time, end_time))
    return history
