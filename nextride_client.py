import os
import json

import wget
import urllib.request
    
def download_static(system):
    system_id = system.id
    remote_id = system.remote_id
    data_dir = f'data/nextride/{system_id}'
    data_path = f'data/nextride/{system_id}/Route.json'
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    wget.download(f'https://nextride.{remote_id}.bctransit.com/api/Route', data_path)

def get_patternids(system):
    system_id = system.id
    remote_id = system.remote_id
    pattern_ids = []

    with open(f'data/nextride/{system_id}/Route.json', 'r') as f:
        routes_list = json.load(f)
    for route in routes_list:
        pattern_ids.append(str(route['patternID']))    
    return pattern_ids
        
def get_bus_mapping(system):
    remote_id = system.remote_id
    
    pattern_ids = get_patternids(system)
    request = f'https://nextride.{remote_id}.bctransit.com/api/VehicleStatuses?patternIds='
    query = ','.join(pattern_ids)
    
    with urllib.request.urlopen(request + query) as response:
        bus_info_json = response.read()
        bus_info_structure = json.loads(bus_info_json)
    
    bus_mapping = {}
    
    for bus in bus_info_structure:
        try:
            fleet_number = str(bus['name'])
            fleet_id = str(bus['vehicleId'])
            bus_mapping[fleet_id] = fleet_number
        except KeyError:
            print('Error: fleet number (name) or fleet id (vehicleId) missing from bus nextride query bus entry')

    return bus_mapping
        
    
    
        
    
    
    

    
    
    