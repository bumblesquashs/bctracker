import json
from datetime import date, datetime

from models.bus_history import BusHistory

LAST_SEEN_PATH = 'data/history/last_seen.json'

last_seen = {}

def update_last_seen(buses):
    for bus in buses:
        position = bus.position
        if bus.number is None or not position.active or position.trip is None:
            continue
        history_date = date.today()
        system_id = position.system.id
        feed_version = position.system.feed_version
        block_id = position.trip.block.id
        routes = [r.number for r in position.trip.block.routes]
        
        last_seen[bus.number] = BusHistory(history_date, bus.id, bus.number, system_id, feed_version, block_id, routes)
    save_last_seen()

def save_last_seen():
    last_seen_data = {
        'last_seen': [h.__dict__() for h in last_seen.values()]
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
        history_date = datetime.strptime(data['date'], '%Y-%m-%d')
        bus_id = data['bus_id']
        number = data['number']
        system_id = data['system_id']
        feed_version = data['feed_version']
        block_id = data['block_id']
        routes = data['routes']

        last_seen[number] = BusHistory(history_date, bus_id, number, system_id, feed_version, block_id, routes)

def all_last_seen():
    return sorted(last_seen.values())
