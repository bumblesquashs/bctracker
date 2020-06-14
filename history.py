import os
import json
from datetime import date, datetime, timedelta
import realtime as rt
import datastructure as ds

VEHICLE_JSON_SEED = '''{"block_history": [{
		"blockid": "0",
		"day": "1969-01-01",
		"routes": ["1", "2", "3", "4"],
        "start_time": "9:00"
	}]}'''

#this is today from 4am - 11:59 and then yesterday from midnight - 3:59 am
def get_service_day():
    hour = datetime.now().hour
    today = date.today()
    if(hour < 5):
        return today - timedelta(days = 1)
    else:
        return today

def update_last_seen():
    if(rt.data_valid):
        with open('data/vehicle_history/last_seen.json', 'r') as f:
            last_seen = json.load(f)
        last_seen_times = last_seen['last_times']
        last_seen_blocks = last_seen['last_blocks']
        for fleetid in rt.rtvehicle_dict.keys():
            rt_entry = rt.rtvehicle_dict[fleetid]
            fleetnum = ''
            try:
                fleetnum = rt.id2fleetnum_dict[fleetid]
            except (KeyError, AttributeError):
                continue
            last_seen_times[fleetnum] = {
            'day': str(get_service_day()),
            }
            if(rt_entry.scheduled and rt_entry.blockid != 'NONE'):
                last_seen_blocks[fleetnum] = {
                'blockid': rt_entry.blockid,
                'day': str(get_service_day()),
                'routes': ds.blockdict[rt_entry.blockid].get_block_routes()
                }
        last_seen['last_times'] = last_seen_times
        last_seen['last_blocks'] = last_seen_blocks
        with open('data/vehicle_history/last_seen.json', 'w') as f:
            json.dump(last_seen, f)
        update_history()

def update_history():
    if(rt.data_valid):
        for fleetid in rt.rtvehicle_dict.keys():
            rt_entry = rt.rtvehicle_dict[fleetid]
            if(not rt_entry.scheduled):
                continue
            fleetnum = ''
            try:
                fleetnum = rt.id2fleetnum_dict[fleetid]
            except (KeyError, AttributeError):
                continue
            fpath = 'data/vehicle_history/vehicle/{0}.json'.format(fleetnum)
            if (not os.path.isfile(fpath)):
                with open(fpath, 'w') as f:
                    f.write(VEHICLE_JSON_SEED)
            skip = False
            with open(fpath, 'r') as f:
                history_data = json.load(f)
            last_blocks = history_data['block_history']
            for block in last_blocks:
                if((block['blockid'] == rt_entry.blockid) and block['day'] == str(get_service_day())):
                    skip = True
                    break
            if(skip): # dont add this block to the history - its a dupe
                continue
            try:
                block = ds.blockdict[rt_entry.blockid]
                routes_str = block.get_block_routes()
                start_time_str = block.get_block_start_time()
            except KeyError:
                routes_str = '(Unknown)'
                start_time_str = ''
            last_blocks.append({
                'blockid': rt_entry.blockid,
                'day': str(get_service_day()),
                'routes': routes_str,
                'start_time': start_time_str
            })
            history_data['block_history'] = last_blocks
            with open(fpath, 'w') as f:
                json.dump(history_data, f)

def get_last_seen():
    with open('data/vehicle_history/last_seen.json', 'r') as f:
        last_seen = json.load(f)
    return last_seen

def get_last_seen_bus(fleetnum):
    with open('data/vehicle_history/last_seen.json', 'r') as f:
        last_seen = json.load(f)
        last_seen_times = last_seen['last_times']
        try:
            return last_seen_times[fleetnum]
        except KeyError:
            return False

#returns false for nonexistant last block history
def get_last_block_bus(fleetnum):
    with open('data/vehicle_history/last_seen.json', 'r') as f:
        last_seen = json.load(f)
    last_seen_blocks = last_seen['last_blocks']
    try:
        return last_seen_blocks[fleetnum]
    except KeyError:
        return False

#returns false for nonexistant block history
def get_block_history(fleetnum):
    if(' ' in fleetnum or '/' in fleetnum):
        return False
    try:
        with open('data/vehicle_history/vehicle/{0}.json'.format(fleetnum), 'r') as f:
            history_data = json.load(f)
        last_blocks = history_data['block_history']
    except FileNotFoundError:
        print('File not found for fleetnum ' + fleetnum)
        return False
    return last_blocks
