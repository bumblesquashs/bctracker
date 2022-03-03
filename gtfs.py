from os import path, rename
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree
from random import randint, seed, shuffle

import wget
import csv

from models.block import Block
from models.departure import Departure
from models.route import Route
from models.service import Service, Sheet
from models.shape import Shape
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
    for values in read_csv(system, 'stop_times'):
        stop_id = values['stop_id']
        if stop_id not in system.stops:
            print(f'Invalid stop id: {stop_id}')
            continue
        trip_id = values['trip_id']
        if trip_id not in system.trips:
            continue
        time_string = values['departure_time']
        sequence = int(values['stop_sequence'])
        
        departure = Departure(system, stop_id, trip_id, time_string, sequence)
        
        departure.stop.add_departure(departure)
        departure.trip.add_departure(departure)

def load_routes(system):
    system.routes = {}
    system.routes_by_number = {}
    for values in read_csv(system, 'routes'):
        route_id = values['route_id']
        number = values['route_short_name']
        name = values['route_long_name']
        if 'route_color' in values and values['route_color'] != '000000':
            colour = values['route_color']
        else:
            # Generate a random colour based on system ID and route number
            seed(system.id + number)
            values = [randint(0, 100), randint(0, 255), randint(100, 255)]
            shuffle(values)
            colour = f'{values[0]:02x}{values[1]:02x}{values[2]:02x}'
        
        route = Route(system, route_id, number, name, colour)
        
        system.routes[route_id] = route
        system.routes_by_number[number] = route

def load_services(system):
    system.services = {}
    for values in read_csv(system, 'calendar'):
        service_id = values['service_id']
        start_date = formatting.csv(values['start_date'])
        end_date = formatting.csv(values['end_date'])
        mon = values['monday'] == '1'
        tue = values['tuesday'] == '1'
        wed = values['wednesday'] == '1'
        thu = values['thursday'] == '1'
        fri = values['friday'] == '1'
        sat = values['saturday'] == '1'
        sun = values['sunday'] == '1'
        
        system.services[service_id] = Service(system, service_id, start_date, end_date, mon, tue, wed, thu, fri, sat, sun)
    for values in read_csv(system, 'calendar_dates'):
        service_id = values['service_id']
        exception_type = int(values['exception_type'])
        
        service = system.get_service(service_id)
        if service is None:
            continue
        
        date = formatting.csv(values['date'])
        if exception_type == 1:
            service.add_included_date(date)
        if exception_type == 2:
            service.add_excluded_date(date)

def load_shapes(system):
    system.shapes = {}
    for values in read_csv(system, 'shapes'):
        shape_id = values['shape_id']
        lat = float(values['shape_pt_lat'])
        lon = float(values['shape_pt_lon'])
        sequence = int(values['shape_pt_sequence'])
        
        shape = system.get_shape(shape_id)
        if shape is None:
            shape = Shape(system, shape_id)
            system.shapes[shape_id] = shape
        
        shape.add_point(lat, lon, sequence)

def load_stops(system):
    system.stops = {}
    system.stops_by_number = {}
    for values in read_csv(system, 'stops'):
        stop_id = values['stop_id']
        try:
            number = int(values['stop_code'])
        except:
            try:
                number = int(stop_id)
            except:
                continue
        name = values['stop_name']
        lat = float(values['stop_lat'])
        lon = float(values['stop_lon'])
        
        stop = Stop(system, stop_id, number, name, lat, lon)
        
        system.stops[stop_id] = stop
        system.stops_by_number[number] = stop

def load_trips(system):
    system.trips = {}
    system.blocks = {}
    for values in read_csv(system, 'trips'):
        trip_id = values['trip_id']
        route_id = values['route_id']
        if route_id not in system.routes:
            print(f'Invalid route id: {route_id}')
            continue
        service_id = values['service_id']
        if service_id not in system.services:
            print(f'Invalid service id: {service_id}')
            continue
        block_id = values['block_id']
        if 'direction_id' in values:
            direction_id = int(values['direction_id'])
        else:
            direction_id = 0
        shape_id = values['shape_id']
        headsign = values['trip_headsign']
        
        trip = Trip(system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign)
        
        if trip.service.sheet != Sheet.CURRENT:
            continue
        
        if block_id not in system.blocks:
            system.blocks[block_id] = Block(system, block_id)
        
        system.trips[trip_id] = trip
        
        trip.block.add_trip(trip)
        trip.route.add_trip(trip)

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
    end_date = None
    for service in system.get_services(None):
        date = service.end_date.date()
        if end_date is None or date > end_date:
            end_date = date
    if end_date is None:
        return False
    return datetime.now().date() < end_date - timedelta(days=7)
