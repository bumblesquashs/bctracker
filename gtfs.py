from os import path, rename
from datetime import date
from zipfile import ZipFile
from shutil import rmtree

import wget

def update(system_id):
    downloads_path = f'downloads/gtfs/{system_id}.zip'
    data_path = f'data/gtfs/{system_id}'

    try:
        if path.exists(downloads_path):
            formatted_date = date.today().strftime('%Y-%m-%d')
            archives_path = f'archives/gtfs/{system_id}-{formatted_date}.zip'
            rename(downloads_path, archives_path)
        wget.download(f'http://{system_id}.mapstrat.com/current/google_transit.zip', downloads_path)
        if path.exists(data_path):
            rmtree(data_path)
        with ZipFile(downloads_path) as zip:
            zip.extractall(data_path)
    except Exception as err:
        print(err)