
from os import path, rename
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree

import wget
import csv

from models.block import Block
from models.date import Date
from models.departure import Departure
from models.route import Route
from models.service import Service
from models.shape import Shape, ShapePoint
from models.sheet import create_sheets
from models.stop import Stop
from models.trip import Trip

def downloaded(system):
    if not system.gtfs_enabled:
        return True
    return path.exists(f'data/gtfs/{system.id}')

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

def load(system):
    if not system.gtfs_enabled:
        return
    print(f'Loading GTFS data for {system}...')
    services = [Service(system, row) for row in read_csv(system, 'calendar')]
    system.services = {s.id: s for s in services}
    
    load_service_exceptions(system)
    
    sheets = create_sheets(services)
    system.sheets = {service.id: sheet for sheet in sheets for service in sheet.services}
    
    points = [ShapePoint.from_csv(row) for row in read_csv(system, 'shapes')]
    shape_points = {}
    for point in points:
        shape_points.setdefault(point.shape_id, []).append(point)
    system.shapes = {id: Shape(system, id, points) for id, points in shape_points.items()}
    
    departures = [Departure.from_csv(row, system) for row in read_csv(system, 'stop_times')]
    trip_departures = {}
    stop_departures = {}
    for departure in departures:
        trip_departures.setdefault(departure.trip_id, []).append(departure)
        stop_departures.setdefault(departure.stop_id, []).append(departure)
    
    trips = [Trip.from_csv(row, system, trip_departures) for row in read_csv(system, 'trips')]
    system.trips = {t.id: t for t in trips}
    
    stops = [Stop.from_csv(row, system, stop_departures) for row in read_csv(system, 'stops')]
    system.stops = {s.id: s for s in stops}
    system.stops_by_number = {s.number: s for s in stops}
    
    route_trips = {}
    block_trips = {}
    for trip in trips:
        route_trips.setdefault(trip.route_id, []).append(trip)
        block_trips.setdefault(trip.block_id, []).append(trip)
    
    routes = [Route.from_csv(row, system, route_trips) for row in read_csv(system, 'routes')]
    system.routes = {r.id: r for r in routes}
    system.routes_by_number = {r.number: r for r in routes}
    
    system.blocks = {id: Block(system, id, trips) for id, trips in block_trips.items()}
    
    print('Done!')

def load_service_exceptions(system):
    for row in read_csv(system, 'calendar_dates'):
        service_id = row['service_id']
        exception_type = int(row['exception_type'])
        
        service = system.get_service(service_id)
        if service is None:
            continue
        
        date = Date.parse_csv(row['date'])
        if exception_type == 1:
            service.include(date)
        if exception_type == 2:
            service.exclude(date)

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
    today = Date.today()
    return today < max(end_dates) - timedelta(days=7)
