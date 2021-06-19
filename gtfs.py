from os import path, rename
from datetime import datetime
from zipfile import ZipFile
from shutil import rmtree

import wget

def update(system):
    data_zip_path = f'data/gtfs/{system.id}.zip'
    data_path = f'data/gtfs/{system.id}'

    try:
        if path.exists(data_zip_path):
            formatted_date = datetime.now().strftime('%Y-%m-%d')
            archives_path = f'archives/gtfs/{system.id}_{formatted_date}.zip'
            rename(data_zip_path, archives_path)
        if system.supports_realtime:
            wget.download(f'http://{system.remote_id}.mapstrat.com/current/google_transit.zip', data_zip_path)
        else:
            wget.download(f'http://bctransit.com/data/gtfs/{system.remote_id}.zip', data_zip_path)
        if path.exists(data_path):
            rmtree(data_path)
        with ZipFile(data_zip_path) as zip:
            zip.extractall(data_path)
    except Exception as e:
        print(f'Error: Failed to update GTFS for {system}')
        print(f'Error message: {e}')

def downloaded(system):
    return path.exists(f'data/gtfs/{system.id}')
