from os import path, rename
from datetime import date
from zipfile import ZipFile
from shutil import rmtree

import wget

def update(system):
    system_id = system.system_id
    remote_id = system.remote_id

    downloads_path = f'downloads/gtfs/{system_id}.zip'
    data_path = f'data/gtfs/{system_id}'

    try:
        if path.exists(downloads_path):
            formatted_date = date.today().strftime('%Y-%m-%d')
            archives_path = f'archives/gtfs/{system_id}-{formatted_date}.zip'
            rename(downloads_path, archives_path)
        if system.supports_realtime:
            wget.download(f'http://{remote_id}.mapstrat.com/current/google_transit.zip', downloads_path)
        else:
            wget.download(f'http://bctransit.com/data/gtfs/{remote_id}.zip', downloads_path)
        if path.exists(data_path):
            rmtree(data_path)
        with ZipFile(downloads_path) as zip:
            zip.extractall(data_path)
    except Exception as err:
        print(err)