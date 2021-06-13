from os import rename, path
from datetime import datetime

import wget

def update(system):
    if not system.supports_realtime:
        return
    
    system_id = system.id
    remote_id = system.remote_id

    downloads_path = f'downloads/realtime/{system_id}.bin'

    try:
        if path.exists(downloads_path):
            formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
            archives_path = f'archives/realtime/{system_id}-{formatted_date}.bin'
            rename(downloads_path, archives_path)
        wget.download(f'http://{remote_id}.mapstrat.com/current/gtfrealtime_VehiclePositions.bin', downloads_path)
    except Exception as err:
        print(err)
