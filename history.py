import json
from datetime import datetime, timedelta

from models.block_history import BlockHistory
from models.bus_history import BusHistory
from models.service import Sheet
from models.time import Time
import database

def update(buses):
    for bus in buses:
        update_bus_history(bus)
    database.commit()

def get_last_seen():
    return []

def update_bus_history(bus):
    position = bus.position
    if bus.number is None or not position.active or position.trip is None:
        return
    history = load_bus_history(bus.number, limit=1)
    hour = datetime.now().hour
    today = datetime.today()
    date = today if hour >= 5 else today - timedelta(days=1)
    block = position.trip.block
    if len(history) > 0:
        last_update = history[0]
        if last_update.date.date() == date.date() and last_update.block_id == block.id:
            return
    system_id = position.system.id
    feed_version = position.system.feed_version
    block_id = block.id
    routes = [r.number for r in block.get_routes(Sheet.CURRENT)]
    routes_string = ', '.join([str(r) for r in routes])
    start_time = block.get_start_time(Sheet.CURRENT)
    end_time = block.get_end_time(Sheet.CURRENT)
    
    bus_history = BlockHistory(date, system_id, feed_version, block_id, routes_string, start_time, end_time)
    
    data = bus_history.json_data
    data['bus_number'] = bus.number
    
    database.insert('bus_history', data)

def load_bus_history(number, limit=None):
    history_data = database.select('bus_history', 
        columns=['date', 'system_id', 'feed_version', 'block_id', 'routes', 'start_time', 'end_time'],
        filters={
            'bus_number': number
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
        
        history.append(BlockHistory(date, system_id, feed_version, block_id, routes, start_time, end_time))
    return history

def load_bus_history_old(number):
    data_path = f'data/history/{number}.json'
    try:
        with open(data_path, 'r') as file:
            history_data = json.load(file)
    except:
        history_data = {}
    history = []
    for data in history_data.get('history', []):
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        system_id = data['system_id']
        feed_version = data['feed_version']
        block_id = data['block_id']
        routes = data['routes']
        start_time = Time(data['start_time'])
        end_time = Time(data['end_time'])
        
        history.append(BlockHistory(date, system_id, feed_version, block_id, routes, start_time, end_time))
    return history
