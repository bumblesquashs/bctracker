
import requests

import protobuf.data.gtfs_realtime_pb2 as protobuf

import helpers.alert

import database

def download(system):
    '''Downloads alerts for the given system'''
    if not system.alerts_enabled:
        return
    
    print(f'Updating alerts data for {system}')
    
    try:
        data = protobuf.FeedMessage()
        with requests.get(system.alerts_url, timeout=10) as r:
            data.ParseFromString(r.content)
        helpers.alert.delete_all(system)
        for entity in data.entity:
            helpers.alert.create(system, entity.id, entity.alert)
        database.commit()
    except Exception as e:
        print(f'Failed to update alerts for {system}: {e}')
