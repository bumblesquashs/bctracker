import os
import json
from datetime import date, datetime, timedelta
import realtime as rt
import datastructure as ds

# seed json data for each bus - this is marked with blockid str '0' and we check
# that in the rendering - it won't ever get shown
VEHICLE_JSON_SEED = '''{"block_history": [{
		"blockid": "0",
		"day": "1969-01-01",
		"routes": ["1", "2", "3", "4"],
        "start_time": "9:00",
        "length": "6"
	}]}'''

# this is today from 4am - 11:59 and then yesterday from midnight - 3:59 am
# handle busses that are out past midnight so they dont get recorded as being from the next day
def get_service_day():
    hour = datetime.now().hour
    today = date.today()
    if(hour < 5):
        return today - timedelta(days = 1)
    else:
        return today

# based on the loaded realtime data, update all the history files
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

# update the block history files for each bus (called from the above)
def update_history():
    if(rt.data_valid):
        print('HISTORY: Updating history!')
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
                length_str = block.get_block_length()
            except KeyError:
                routes_str = '(Unknown)'
                start_time_str = ''
            last_blocks.append({
                'blockid': rt_entry.blockid,
                'day': str(get_service_day()),
                'routes': routes_str,
                'start_time': start_time_str,
                'length': length_str,
            })
            history_data['block_history'] = last_blocks
            with open(fpath, 'w') as f:
                json.dump(history_data, f)

# ------------------------------------------------------------------------------
# The old system: one json file with the last seen times and blocks for all known busses
# we keep this around since some busses retired before the new system saw them
# ------------------------------------------------------------------------------

# read out what's in the general last seen history file (contains last seen for all busses)
def get_last_seen():
    with open('data/vehicle_history/last_seen.json', 'r') as f:
        last_seen = json.load(f)
    return last_seen

# from the general file, pick out the last seen time for a particular fleet num
# returns false for nonexistant bus in the history
def get_last_seen_bus(fleetnum):
    with open('data/vehicle_history/last_seen.json', 'r') as f:
        last_seen = json.load(f)
        last_seen_times = last_seen['last_times']
        try:
            return last_seen_times[fleetnum]
        except KeyError:
            return False
# from the general file, get the last seen block for a particular fleet num
# returns false for nonexistant bus last block history
def get_last_block_bus(fleetnum):
    with open('data/vehicle_history/last_seen.json', 'r') as f:
        last_seen = json.load(f)
    last_seen_blocks = last_seen['last_blocks']
    try:
        return last_seen_blocks[fleetnum]
    except KeyError:
        return False

# ------------------------------------------------------------------------------
# The new system: keep a history of blocks for each bus, one json file per bus
# ------------------------------------------------------------------------------

# get the whole block history for a bus (based on its specific file)
# returns false for nonexistant block history
def get_block_history(fleetnum):
    try:
        with open('data/vehicle_history/vehicle/{0}.json'.format(fleetnum), 'r') as f:
            history_data = json.load(f)
        last_blocks = history_data['block_history']
    except FileNotFoundError:
        print('File not found for fleetnum ' + fleetnum)
        return False
    return last_blocks

# get the time string given block start time and length
def get_time_string(start_time_str, length_str):
    start_hour = int(start_time_str.split(':')[0])
    if(start_hour > 12):
        if(int(length_str) < 5):
            return 'PM Tripper'
        return 'Evening'
    if(int(length_str) > 4):
        return 'All Day'
    return 'AM Tripper'
