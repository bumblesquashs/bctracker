
from os import path, rename, remove
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree
from threading import Thread

import csv
import requests

from di import di

from models.block import Block
from models.date import Date
from models.service import Service, ServiceException

from services import Config, DepartureService, GTFSService, PointService, RouteService, SheetService, StopService, TripService

class DefaultGTFSService(GTFSService):
    
    __slots__ = (
        'config',
        'departure_service',
        'point_service',
        'route_service',
        'sheet_service',
        'stop_service',
        'trip_service'
    )
    
    def __init__(self, **kwargs):
        self.config = kwargs.get('config') or di[Config]
        self.departure_service = kwargs.get('departure_service') or di[DepartureService]
        self.point_service = kwargs.get('point_service') or di[PointService]
        self.route_service = kwargs.get('route_service') or di[RouteService]
        self.sheet_service = kwargs.get('sheet_service') or di[SheetService]
        self.stop_service = kwargs.get('stop_service') or di[StopService]
        self.trip_service = kwargs.get('trip_service') or di[TripService]
    
    def load(self, system, force_download=False, update_db=False):
        '''Loads the GTFS for the given system into memory'''
        if not system.gtfs_enabled:
            return
        if not path.exists(f'data/gtfs/{system.id}') or force_download:
            self.download(system)
            self.update_database(system)
        elif update_db:
            self.update_database(system)
        
        print(f'Loading GTFS data for {system}')
        try:
            exceptions = read_csv(system, 'calendar_dates', lambda r: ServiceException.from_csv(r, system))
            service_exceptions = {}
            for exception in exceptions:
                service_exceptions.setdefault(exception.service_id, []).append(exception)
            
            try:
                services = read_csv(system, 'calendar', lambda r: Service.from_csv(r, system, service_exceptions))
            except:
                services = [Service.combine(system, service_id, exceptions) for (service_id, exceptions) in service_exceptions.items()]
            
            system.services = {s.id: s for s in services}
            system.sheets = self.sheet_service.combine(system, services)
            
            stops = self.stop_service.find_all(system.id)
            system.stops = {s.id: s for s in stops}
            system.stops_by_number = {s.number: s for s in stops}
            
            trips = self.trip_service.find_all(system.id)
            system.trips = {t.id: t for t in trips}
            
            block_trips = {}
            for trip in trips:
                block_trips.setdefault(trip.block_id, []).append(trip)
            
            routes = self.route_service.find_all(system.id)
            system.routes = {r.id: r for r in routes}
            system.routes_by_number = {r.number: r for r in routes}
            
            system.blocks = {id: Block(system, id, trips) for id, trips in block_trips.items()}
            
            system.gtfs_loaded = True
        except Exception as e:
            print(f'Failed to load GTFS for {system}: {e}')
    
    def download(self, system):
        '''Downloads the GTFS for the given system'''
        if not system.gtfs_enabled:
            return
        data_zip_path = f'data/gtfs/{system.id}.zip'
        data_path = f'data/gtfs/{system.id}'
        
        print(f'Downloading GTFS data for {system}')
        try:
            if path.exists(data_zip_path):
                if self.config.enable_gtfs_backups:
                    formatted_date = datetime.now().strftime('%Y-%m-%d')
                    archives_path = f'archives/gtfs/{system.id}_{formatted_date}.zip'
                    rename(data_zip_path, archives_path)
                else:
                    remove(data_zip_path)
            with requests.get(system.gtfs_url, stream=True) as r:
                with open(data_zip_path, 'wb') as f:
                    for chunk in r.iter_content(128):
                        f.write(chunk)
            if path.exists(data_path):
                rmtree(data_path)
            with ZipFile(data_zip_path) as zip:
                zip.extractall(data_path)
        except Exception as e:
            print(f'Failed to download GTFS for {system}: {e}')
    
    def update_database(self, system):
        '''Updates cached GTFS data for the given system'''
        if not system.gtfs_enabled:
            return
        print(f'Updating database with GTFS data for {system}')
        try:
            self.departure_service.delete_all(system)
            self.trip_service.delete_all(system)
            self.stop_service.delete_all(system)
            self.route_service.delete_all(system)
            self.point_service.delete_all(system)
            
            apply_csv(system, 'routes', self.route_service.create)
            apply_csv(system, 'stops', self.stop_service.create)
            apply_csv(system, 'trips', self.trip_service.create)
            apply_csv(system, 'stop_times', self.departure_service.create)
            apply_csv(system, 'shapes', self.point_service.create)
        except Exception as e:
            print(f'Failed to update GTFS for {system}: {e}')
    
    def validate(self, system):
        '''Checks that the GTFS for the given system is up-to-date'''
        if not system.gtfs_enabled:
            return True
        end_dates = [s.schedule.date_range.end for s in system.get_services()]
        if len(end_dates) == 0:
            return True
        return Date.today(system.timezone) < max(end_dates) - timedelta(days=7)
    
    def update_cache_in_background(self, system):
        '''Updates cached data for the given system in a background thread'''
        thread = Thread(target=system.update_cache)
        thread.start()

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
