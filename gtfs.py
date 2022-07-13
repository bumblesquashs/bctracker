
from os import path, rename
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree

import wget
import csv

import helpers.sheet

from models.block import Block
from models.date import Date
from models.departure import Departure
from models.route import Route
from models.service import Service, ServiceException
from models.shape import Shape, ShapePoint
from models.stop import Stop
from models.trip import Trip

def downloaded(system):
    '''Checks that the GTFS is downloaded for the given system'''
    return path.exists(f'data/gtfs/{system.id}')

def update(system):
    '''Downloads the GTFS for the given system, then loads it into memory'''
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
    '''Loads the GTFS for the given system into memory'''
    if not system.gtfs_enabled:
        return
    print(f'Loading GTFS data for {system}...')
    
    agencies = read_csv(system, 'agency', lambda r: r)
    if len(agencies) > 0:
        agency = agencies[0]
        if 'agency_timezone' in agency:
            system.timezone = agency['agency_timezone']
    
    exceptions = read_csv(system, 'calendar_dates', ServiceException.from_csv)
    service_exceptions = {}
    for exception in exceptions:
        service_exceptions.setdefault(exception.service_id, []).append(exception)
    
    services = read_csv(system, 'calendar', lambda r: Service.from_csv(r, system, service_exceptions))
    system.services = {s.id: s for s in services}
    
    sheets = helpers.sheet.combine(services)
    system.sheets = {service.id: sheet for sheet in sheets for service in sheet.services}
    
    points = read_csv(system, 'shapes', ShapePoint.from_csv)
    shape_points = {}
    for point in points:
        shape_points.setdefault(point.shape_id, []).append(point)
    system.shapes = {id: Shape(system, id, points) for id, points in shape_points.items()}
    
    departures = read_csv(system, 'stop_times', lambda r: Departure.from_csv(r, system))
    trip_departures = {}
    stop_departures = {}
    for departure in departures:
        trip_departures.setdefault(departure.trip_id, []).append(departure)
        stop_departures.setdefault(departure.stop_id, []).append(departure)
    
    trips = read_csv(system, 'trips', lambda r: Trip.from_csv(r, system, trip_departures))
    system.trips = {t.id: t for t in trips}
    
    stops = read_csv(system, 'stops', lambda r: Stop.from_csv(r, system, stop_departures))
    system.stops = {s.id: s for s in stops}
    system.stops_by_number = {s.number: s for s in stops}
    
    route_trips = {}
    block_trips = {}
    for trip in trips:
        route_trips.setdefault(trip.route_id, []).append(trip)
        block_trips.setdefault(trip.block_id, []).append(trip)
    
    routes = read_csv(system, 'routes', lambda r: Route.from_csv(r, system, route_trips))
    system.routes = {r.id: r for r in routes}
    system.routes_by_number = {r.number: r for r in routes}
    
    system.blocks = {id: Block(system, id, trips) for id, trips in block_trips.items()}
    
    print('Done!')

def read_csv(system, name, initializer):
    '''Opens a CSV file and applies an initializer to each row'''
    with open(f'./data/gtfs/{system.id}/{name}.txt', 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        columns = next(reader)
        return [initializer(dict(zip(columns, row))) for row in reader]

def validate(system):
    '''Checks that the GTFS for the given system is up-to-date'''
    if not system.gtfs_enabled:
        return True
    end_dates = [s.end_date for s in system.services.values()]
    if len(end_dates) == 0:
        return True
    return Date.today(system) < max(end_dates) - timedelta(days=7)
