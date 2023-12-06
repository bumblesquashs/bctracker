
from os import path, rename
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree

import csv
import requests

import helpers.departure
import helpers.point
import helpers.sheet

from models.block import Block
from models.date import Date
from models.departure import Departure
from models.point import Point
from models.route import Route
from models.service import Service, ServiceException
from models.stop import Stop
from models.trip import Trip

def load(system, force_download=False, update_db=False):
    '''Loads the GTFS for the given system into memory'''
    if not system.gtfs_enabled:
        return
    if not path.exists(f'data/gtfs/{system.id}') or force_download:
        download(system)
        update_database(system)
    elif update_db:
        update_database(system)
    print(f'Loading GTFS data for {system}...', end=' ', flush=True)
    
    try:
        agencies = read_csv(system, 'agency', lambda r: r)
        if len(agencies) > 0:
            agency = agencies[0]
            if 'agency_timezone' in agency:
                system.timezone = agency['agency_timezone']
        
        exceptions = read_csv(system, 'calendar_dates', lambda r: ServiceException.from_csv(r, system))
        service_exceptions = {}
        for exception in exceptions:
            service_exceptions.setdefault(exception.service_id, []).append(exception)
        
        try:
            services = read_csv(system, 'calendar', lambda r: Service.from_csv(r, system, service_exceptions))
        except:
            services = [Service.combine(system, service_id, exceptions) for (service_id, exceptions) in service_exceptions.items()]
        
        system.services = {s.id: s for s in services}
        system.sheets = helpers.sheet.combine(system, services)
        
        departures = helpers.departure.find_all(system.id)
        trip_departures = {}
        stop_departures = {}
        for departure in departures:
            trip_departures.setdefault(departure.trip_id, []).append(departure)
            stop_departures.setdefault(departure.stop_id, []).append(departure)
        
        stops = read_csv(system, 'stops', lambda r: Stop.from_csv(r, system))
        system.stops = {s.id: s for s in stops}
        system.stops_by_number = {s.number: s for s in stops}
        
        trips = read_csv(system, 'trips', lambda r: Trip.from_csv(r, system, trip_departures))
        system.trips = {t.id: t for t in trips}
        
        for stop in system.stops.values():
            stop.setup(stop_departures.get(stop.id, []))
        
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
    except Exception as e:
        print('Error!')
        print(f'  Failed to load GTFS for {system}: {e}')

def download(system):
    '''Downloads the GTFS for the given system, then loads it into memory'''
    if not system.gtfs_enabled:
        return
    data_zip_path = f'data/gtfs/{system.id}.zip'
    data_path = f'data/gtfs/{system.id}'
    
    print(f'Downloading GTFS data for {system}...', end=' ', flush=True)
    
    try:
        if path.exists(data_zip_path):
            formatted_date = datetime.now().strftime('%Y-%m-%d')
            archives_path = f'archives/gtfs/{system.id}_{formatted_date}.zip'
            rename(data_zip_path, archives_path)
        with requests.get(system.gtfs_url, stream=True) as r:
            with open(data_zip_path, 'wb') as f:
                for chunk in r.iter_content(128):
                    f.write(chunk)
        if path.exists(data_path):
            rmtree(data_path)
        with ZipFile(data_zip_path) as zip:
            zip.extractall(data_path)
        print('Done!')
    except Exception as e:
        print('Error!')
        print(f'  Failed to download GTFS for {system}: {e}')

def update_database(system):
    print(f'Updating database with GTFS data for {system}...', end=' ', flush=True)
    try:
        helpers.departure.delete_all(system)
        helpers.point.delete_all(system)
        
        apply_csv(system, 'stop_times', helpers.departure.create)
        apply_csv(system, 'shapes', helpers.point.create)
        
        print('Done!')
    except Exception as e:
        print('Error!')
        print(f'  Failed to update GTFS for {system}: {e}')

def read_csv(system, name, initializer):
    '''Opens a CSV file and applies an initializer to each row'''
    with open(f'./data/gtfs/{system.id}/{name}.txt', 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        columns = next(reader)
        return [initializer(dict(zip(columns, row))) for row in reader]

def apply_csv(system, name, function):
    '''Opens a CSV file and applies a function to each row'''
    with open(f'./data/gtfs/{system.id}/{name}.txt', 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            function(system, dict(zip(columns, row)))

def validate(system):
    '''Checks that the GTFS for the given system is up-to-date'''
    if not system.gtfs_enabled:
        return True
    end_dates = [s.schedule.date_range.end for s in system.get_services()]
    if len(end_dates) == 0:
        return True
    return Date.today(system.timezone) < max(end_dates) - timedelta(days=7)
