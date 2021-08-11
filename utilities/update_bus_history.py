#!/usr/bin/env python

from os import listdir, path
import json

for file_name in listdir('vehicle_history'):
    old_path = f'vehicle_history/{file_name}'
    new_path = f'data/history/{file_name}'
    
    with open(old_path, 'r') as file:
        old_data = json.load(file)
    
    new_data = []
    
    for value in old_data['block_history']:
        if value['blockid'] == '0':
            continue
        new_data.append({
            'date': value['day'],
            'system_id': 'victoria',
            'feed_version': '',
            'block_id': value['blockid'],
            'routes': [int(r) for r in value['routes']],
            'start_time': value['start_time'],
            'end_time': ''
        })
    
    with open(new_path, 'w') as file:
        json.dump({ 'history': new_data }, file)
