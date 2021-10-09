import json
from datetime import datetime, timedelta

from models.block_history import BlockHistory
from models.bus_history import BusHistory
from models.service import Sheet
from models.time import Time

LAST_SEEN_PATH = 'data/history/last_seen.json'

last_seen = {}

def update(buses):
    update_last_seen(buses)
    for bus in buses:
        update_bus_history(bus)

def update_last_seen(buses):
    for bus in buses:
        position = bus.position
        if bus.number is None or not position.active or position.trip is None:
            continue
        trip = position.trip
        date = datetime.today()
        system_id = position.system.id
        feed_version = position.system.feed_version
        block_id = trip.block.id
        routes = [r.number for r in trip.block.get_routes(Sheet.CURRENT)]
        
        last_seen[bus.number] = BusHistory(date, bus.id, bus.number, system_id, feed_version, block_id, routes)
    save_last_seen()

def save_last_seen():
    last_seen_data = {
        'last_seen': [h.json_data for h in last_seen.values()]
    }
    with open(LAST_SEEN_PATH, 'w') as file:
        json.dump(last_seen_data, file)

def load_last_seen():
    global last_seen
    try:
        with open(LAST_SEEN_PATH, 'r') as file:
            last_seen_data = json.load(file)
    except:
        last_seen_data = {}
    for data in last_seen_data.get('last_seen', []):
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        bus_id = data['bus_id']
        number = data['number']
        system_id = data['system_id']
        feed_version = data['feed_version']
        block_id = data['block_id']
        routes = data['routes']

        last_seen[number] = BusHistory(date, bus_id, number, system_id, feed_version, block_id, routes)

def all_last_seen():
    return sorted(last_seen.values())

def update_bus_history(bus):
    position = bus.position
    if bus.number is None or not position.active or position.trip is None:
        return
    history = load_bus_history(bus.number)
    hour = datetime.now().hour
    today = datetime.today()
    date = today if hour >= 5 else today - timedelta(days=1)
    block = position.trip.block
    if len(history) > 0:
        last_update = history[-1]
        if last_update.date.date() == date.date() and last_update.block_id == block.id:
            return
    system_id = position.system.id
    feed_version = position.system.feed_version
    block_id = block.id
    routes = [r.number for r in block.get_routes(Sheet.CURRENT)]
    start_time = block.get_start_time(Sheet.CURRENT)
    end_time = block.get_end_time(Sheet.CURRENT)
    
    history.append(BlockHistory(date, system_id, feed_version, block_id, routes, start_time, end_time))
    
    data_path = f'data/history/{bus.number}.json'
    history_data = {
        'history': [h.json_data for h in history]
    }
    with open(data_path, 'w') as file:
        json.dump(history_data, file)

def load_bus_history(number):
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
