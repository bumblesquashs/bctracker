from os import path, rename
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree

import wget
import csv

from models.block import Block
from models.route import Route
from models.service import Service
from models.shape import Shape
from models.stop import Stop
from models.stop_time import StopTime
from models.trip import Trip

from formatting import format_csv

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
        if system.realtime_enabled:
            wget.download(f'http://{system.mapstrat_id}.mapstrat.com/current/google_transit.zip', data_zip_path)
        else:
            wget.download(f'http://bctransit.com/data/gtfs/{system.bctransit_id}.zip', data_zip_path)
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
    load_feed_info(system)
    load_stops(system)
    load_routes(system)
    load_services(system)
    load_shapes(system)
    load_trips(system)
    load_stop_times(system)
    system.sort_data()
    print('Done!')

def load_feed_info(system):
    values = read_csv(system, 'feed_info')[0]
    system.feed_version = values['feed_version']

def load_routes(system):
    system.routes = {}
    system.routes_by_number = {}
    for values in read_csv(system, 'routes'):
        route_id = values['route_id']
        number = int(values['route_short_name'])
        name = values['route_long_name']
        if 'route_color' in values:
            colour = values['route_color']
        else:
            colour = '4040FF'

        route = Route(system, route_id, number, name, colour)

        system.routes[route_id] = route
        system.routes_by_number[number] = route

def load_services(system):
    system.services = {}
    for values in read_csv(system, 'calendar'):
        service_id = values['service_id']
        start_date = format_csv(values['start_date'])
        end_date = format_csv(values['end_date'])
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
        
        date = format_csv(values['date'])
        if exception_type == 1:
            service.add_special_date(date)
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
    
def load_stop_times(system):
    for values in read_csv(system, 'stop_times'):
        stop_id = values['stop_id']
        if stop_id not in system.stops:
            print(f'Invalid stop id: {stop_id}')
            continue
        trip_id = values['trip_id']
        if trip_id not in system.trips:
            print(f'Invalid trip id: {trip_id}')
            continue
        time = values['departure_time']
        sequence = int(values['stop_sequence'])

        stop_time = StopTime(system, stop_id, trip_id, time, sequence)

        stop_time.stop.add_stop_time(stop_time)
        stop_time.trip.add_stop_time(stop_time)

def load_stops(system):
    system.stops = {}
    system.stops_by_number = {}
    for values in read_csv(system, 'stops'):
        stop_id = values['stop_id']
        try:
            number = int(values['stop_code'])
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
        if block_id not in system.blocks:
            system.blocks[block_id] = Block(system, block_id)
        direction_id = int(values['direction_id'])
        shape_id = values['shape_id']
        headsign = values['trip_headsign']

        trip = Trip(system, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign)

        system.trips[trip_id] = trip

        trip.block.add_trip(trip)
        trip.route.add_trip(trip)

def read_csv(system, name):
    rows = []
    with open(f'./data/gtfs/{system.id}/{name}.txt', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    return rows

def validate(system):
    if not system.gtfs_enabled:
        return True
    end_date = None
    for service in system.all_services():
        date = service.end_date.date()
        if end_date is None or date > end_date:
            end_date = date
    return datetime.now().date() < end_date - timedelta(days=7)
