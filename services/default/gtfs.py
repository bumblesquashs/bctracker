
from os import path, rename, remove
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree
from threading import Thread

import csv
import requests

from di import di
from config import Config

from models.block import Block
from models.date import Date
from models.daterange import DateRange
from models.service import Service, ServiceException
from models.sheet import Sheet

from repositories import DepartureRepository, PointRepository, RouteRepository, StopRepository, TripRepository
from services import GTFSService

class DefaultGTFSService(GTFSService):
    
    __slots__ = (
        'config',
        'departure_repository',
        'point_repository',
        'route_repository',
        'stop_repository',
        'trip_repository'
    )
    
    def __init__(self, config: Config, **kwargs):
        self.config = config
        self.departure_repository = kwargs.get('departure_repository') or di[DepartureRepository]
        self.point_repository = kwargs.get('point_repository') or di[PointRepository]
        self.route_repository = kwargs.get('route_repository') or di[RouteRepository]
        self.stop_repository = kwargs.get('stop_repository') or di[StopRepository]
        self.trip_repository = kwargs.get('trip_repository') or di[TripRepository]
    
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
            system.sheets = combine_sheets(system, services)
            
            stops = self.stop_repository.find_all(system.id)
            system.stops = {s.id: s for s in stops}
            system.stops_by_number = {s.number: s for s in stops}
            
            trips = self.trip_repository.find_all(system.id)
            system.trips = {t.id: t for t in trips}
            
            block_trips = {}
            for trip in trips:
                block_trips.setdefault(trip.block_id, []).append(trip)
            
            routes = self.route_repository.find_all(system.id)
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
            self.departure_repository.delete_all(system)
            self.trip_repository.delete_all(system)
            self.stop_repository.delete_all(system)
            self.route_repository.delete_all(system)
            self.point_repository.delete_all(system)
            
            apply_csv(system, 'routes', self.route_repository.create)
            apply_csv(system, 'stops', self.stop_repository.create)
            apply_csv(system, 'trips', self.trip_repository.create)
            apply_csv(system, 'stop_times', self.departure_repository.create)
            apply_csv(system, 'shapes', self.point_repository.create)
        except Exception as e:
            print(f'Failed to update GTFS for {system}: {e}')
    
    def validate(self, system):
        '''Checks that the GTFS for the given system is up-to-date'''
        if not system.gtfs_enabled:
            return True
        end_dates = [s.schedule.date_range.end for s in system.get_services()]
        if end_dates:
            return Date.today(system.timezone) < max(end_dates) - timedelta(days=7)
        return True
    
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

def combine_sheets(system, services):
    '''Returns a list of sheets made from services with overlapping start/end dates'''
    if not services:
        return []
    all_date_ranges = {s.schedule.date_range for s in services}
    start_dates = {r.start for r in all_date_ranges}
    end_dates = {r.end for r in all_date_ranges}
    all_start_dates = start_dates.union({d.next() for d in end_dates})
    all_end_dates = end_dates.union({d.previous() for d in start_dates})
    dates = list(all_start_dates) + list(all_end_dates)
    sorted_dates = sorted(dates)[1:-1]
    i = iter(sorted_dates)
    
    sheets = []
    for (start_date, end_date) in zip(i, i):
        date_range = DateRange(start_date, end_date)
        date_range_services = {s for s in services if s.schedule.date_range.overlaps(date_range)}
        if not date_range_services:
            continue
        if sheets:
            previous_sheet = sheets[-1]
            previous_services = {s for s in previous_sheet.services if not s.schedule.is_special}
            current_services = {s for s in date_range_services if not s.schedule.is_special}
            if previous_services.issubset(current_services) or current_services.issubset(previous_services):
                date_range = DateRange.combine([previous_sheet.schedule.date_range, date_range])
                new_services = {s for s in services if s.schedule.date_range.overlaps(date_range)}
                sheets[-1] = Sheet(system, new_services, date_range)
            else:
                sheets.append(Sheet(system, date_range_services, date_range))
        else:
            sheets.append(Sheet(system, date_range_services, date_range))
    final_sheets = []
    for sheet in sheets:
        if final_sheets:
            previous_sheet = final_sheets[-1]
            if len(previous_sheet.schedule.date_range) <= 7 or len(sheet.schedule.date_range) <= 7:
                date_range = DateRange.combine([previous_sheet.schedule.date_range, sheet.schedule.date_range])
                combined_services = previous_sheet.services.union(sheet.services)
                final_sheets[-1] = Sheet(system, combined_services, date_range)
            else:
                final_sheets.append(sheet)
        else:
            final_sheets.append(sheet)
    return final_sheets
