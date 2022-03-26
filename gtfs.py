from os import path, rename
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree

import wget
import csv

from models.block import Block
from models.departure import Departure
from models.route import Route
from models.service import Service
from models.shape import Shape
from models.sheet import create_sheets
from models.stop import Stop
from models.trip import Trip

import formatting

def update(system):
    if not system.gtfs_enabled:
        return
    data_zip_path = f'data/gtfs/{system.id}.zip'
    data_path = f'data/gtfs/{system.id}'
    
    print(f'Updating GTFS data for {system}...')
    
    try:
        if path.exists(data_zip_path):
            formatted_date = datetime.now().strftime('%Y-%m-%d')
            archives_path = f'archives/gtfs/{system.id}_{formatted_date}.zip'
            rename(data_zip_path, archives_path)
        wget.download(system.gtfs_url, data_zip_path)
        if path.exists(data_path):
            rmtree(data_path)
        with ZipFile(data_zip_path) as zip:
            zip.extractall(data_path)
        print('\nDone!')
        load(system)
    except Exception as e:
        print(f'\nError: Failed to update GTFS for {system}')
        print(f'Error message: {e}')

def downloaded(system):
    if not system.gtfs_enabled:
        return True
    return path.exists(f'data/gtfs/{system.id}')

def load(system):
    if not system.gtfs_enabled:
        return
    print(f'Loading GTFS data for {system}...')
    load_stops(system)
    load_routes(system)
    load_services(system)
    load_shapes(system)
    load_trips(system)
    load_departures(system)
    system.sort_data()
    print('Done!')

def load_departures(system):
    for row in read_csv(system, 'stop_times'):
        departure = Departure(system, row)
        stop = departure.stop
        trip = departure.trip
        if stop is None or trip is None:
            continue
        stop.add_departure(departure)
        trip.add_departure(departure)

def load_routes(system):
    system.routes = {}
    system.routes_by_number = {}
    for row in read_csv(system, 'routes'):
        route = Route(system, row)
        
        system.routes[route.id] = route
        system.routes_by_number[route.number] = route

def load_services(system):
    system.services = {}
    for row in read_csv(system, 'calendar'):
        service = Service(system, row)
        system.services[service.id] = service
    for row in read_csv(system, 'calendar_dates'):
        service_id = row['service_id']
        exception_type = int(row['exception_type'])
        
        service = system.get_service(service_id)
        if service is None:
            continue
        
        date = formatting.csv(row['date'])
        if exception_type == 1:
            service.include(date)
        if exception_type == 2:
            service.exclude(date)
    sheets = create_sheets(system.get_services())
    system.sheets = {service.id:sheet for sheet in sheets for service in sheet.services}

def load_shapes(system):
    system.shapes = {}
    for row in read_csv(system, 'shapes'):
        shape_id = row['shape_id']
        lat = float(row['shape_pt_lat'])
        lon = float(row['shape_pt_lon'])
        sequence = int(row['shape_pt_sequence'])
        
        shape = system.get_shape(shape_id)
        if shape is None:
            shape = Shape(system, shape_id)
            system.shapes[shape_id] = shape
        
        shape.add_point(lat, lon, sequence)

def load_stops(system):
    system.stops = {}
    system.stops_by_number = {}
    for row in read_csv(system, 'stops'):
        stop = Stop(system, row)
        
        system.stops[stop.id] = stop
        system.stops_by_number[stop.number] = stop

def load_trips(system):
    system.trips = {}
    system.blocks = {}
    for row in read_csv(system, 'trips'):
        trip = Trip(system, row)
        
        service = trip.service
        route = trip.route
        block = trip.block
        
        if service is None or route is None:
            continue
        if not system.get_sheet(service).is_current:
            continue
        
        route.add_trip(trip)
        
        if block is None:
            system.blocks[trip.block_id] = Block(system, trip)
        else:
            block.add_trip(trip)
        
        system.trips[trip.id] = trip

def read_csv(system, name):
    rows = []
    with open(f'./data/gtfs/{system.id}/{name}.txt', 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    return rows

def validate(system):
    if not system.gtfs_enabled:
        return True
    end_dates = [s.end_date for s in system.get_services()]
    if len(end_dates) == 0:
        return True
    end_date = max(end_dates)
    return datetime.now().date() < end_date - timedelta(days=7)
