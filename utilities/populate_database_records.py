#!/usr/bin/env python
from os import listdir
from os.path import join
import json

import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import database

database.connect()

PATH = './data/history'

for file in listdir(PATH):
    if file == 'last_seen.json':
        continue # deal with last seen separately
    file_path = join(PATH, file)
    
    bus_number = int(str(file)[:-5])
    try:
        with open(file_path, 'r') as file:
            history_data = json.load(file)
    except:
        history_data = {}
    for data in history_data.get('history', []):
        date = data['date']
        system_id = data['system_id']
        block_id = data['block_id']
        routes = data['routes']
        start_time = data['start_time']
        end_time = data['end_time']
        
        routes.sort(key=lambda r: int(''.join([d for d in str(r) if d.isdigit()])))
        
        values = {
            'bus_number': bus_number,
            'date': date,
            'system_id': system_id,
            'block_id': block_id,
            'routes': ', '.join([str(r) for r in routes])
        }
        if start_time != '':
            values['start_time'] = start_time
        if end_time != '':
            values['end_time'] = end_time
        
        database.insert('records', values)

try:
    with open(join(PATH, 'last_seen.json'), 'r') as file:
        last_seen_data = json.load(file)
except:
    last_seen_data = {}
for data in last_seen_data.get('last_seen', []):
    bus_number = data['number']
    date = data['date']
    system_id = data['system_id']
    block_id = data['block_id']
    routes = data['routes']
    
    routes.sort(key=lambda r: int(''.join([d for d in str(r) if d.isdigit()])))
    
    rows = database.select('records',
        columns=['rowid'],
        filters={
            'bus_number': bus_number,
            'date': date,
            'system_id': system_id,
            'block_id': block_id
        })
    if len(rows) > 0:
        continue
    
    values = {
        'bus_number': bus_number,
        'date': date,
        'system_id': system_id,
        'block_id': block_id,
        'routes': ', '.join([str(r) for r in routes])
    }
    database.insert('records', values)

database.commit()
database.disconnect()