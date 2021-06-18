import os
import json
import nextride_client

translation_table_path = 'data/realtime/fleetnumber_translation.json'

# global for speed
fleetnumber_translation_table = {}

def load_table():
    global fleetnumber_translation_table
    try:
        with open(translation_table_path, 'r') as f:
            fleetnumber_translation_table = json.load(f)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}

def save_table():
    with open(translation_table_path, 'w') as f:
        json.dump(fleetnumber_translation_table, f)
    
def get_table():
    return fleetnumber_translation_table
    
def update_table(system):
    load_table()
    bus_mapping = nextride_client.get_bus_mapping(system)
    for fleet_id in bus_mapping.keys():
        fleetnumber_translation_table[fleet_id] = bus_mapping[fleet_id]
    save_table()
