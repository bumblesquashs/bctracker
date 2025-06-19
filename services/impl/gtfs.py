
from os import path, rename, remove
from dataclasses import dataclass
from datetime import datetime, timedelta
from zipfile import ZipFile
from shutil import rmtree
from threading import Thread

import csv
import requests

from database import Database
from settings import Settings

from models.block import Block
from models.context import Context
from models.date import Date
from models.daterange import DateRange
from models.service import Service, ServiceException
from models.sheet import Sheet

import repositories

@dataclass(slots=True)
class GTFSService:
    
    database: Database
    settings: Settings
    
    def load(self, context: Context, force_download=False, update_db=False):
        '''Loads the GTFS for the given context into memory'''
        if not context.system.gtfs_enabled:
            return
        
        context.system.gtfs_downloaded = path.exists(f'data/gtfs/{context.system_id}')
        if not context.system.gtfs_downloaded or force_download:
            self.download(context)
            update_db = True
        
        if update_db:
            self.update_database(context)
        
        print(f'Loading GTFS data for {context}')
        
        exceptions = read_csv(context, 'calendar_dates', lambda r: ServiceException.from_csv(r, context))
        service_exceptions = {}
        for exception in exceptions:
            service_exceptions.setdefault(exception.service_id, []).append(exception)
        
        try:
            services = read_csv(context, 'calendar', lambda r: Service.from_csv(r, context, service_exceptions))
        except:
            services = [Service.combine(context, service_id, exceptions) for (service_id, exceptions) in service_exceptions.items()]
        
        context.system.services = {s.id: s for s in services}
        context.system.sheets = combine_sheets(context, services)
        
        stops = repositories.stop.find_all(context)
        context.system.stops = {s.id: s for s in stops}
        context.system.stops_by_number = {s.number: s for s in stops}
        
        trips = repositories.trip.find_all(context)
        context.system.trips = {t.id: t for t in trips}
        
        block_trips = {}
        for trip in trips:
            block_trips.setdefault(trip.block_id, []).append(trip)
        
        routes = repositories.route.find_all(context)
        context.system.routes = {r.id: r for r in routes}
        context.system.routes_by_number = {r.number: r for r in routes}
        
        context.system.blocks = {id: Block(context.system, id, trips) for id, trips in block_trips.items()}
        
        context.system.gtfs_loaded = True
    
    def download(self, context: Context):
        '''Downloads the GTFS for the given system'''
        print(f'Downloading GTFS data for {context}')
        
        data_zip_path = f'data/gtfs/{context.system_id}.zip'
        data_path = f'data/gtfs/{context.system_id}'
        
        if path.exists(data_zip_path):
            if self.settings.enable_gtfs_backups:
                formatted_date = datetime.now().strftime('%Y-%m-%d')
                archives_path = f'archives/gtfs/{context.system_id}_{formatted_date}.zip'
                rename(data_zip_path, archives_path)
            else:
                remove(data_zip_path)
            context.system.gtfs_downloaded = False
        with requests.get(context.system.gtfs_url, stream=True) as r:
            with open(data_zip_path, 'wb') as f:
                for chunk in r.iter_content(128):
                    f.write(chunk)
        if path.exists(data_path):
            rmtree(data_path)
        with ZipFile(data_zip_path) as zip:
            zip.extractall(data_path)
        context.system.gtfs_downloaded = True
    
    def update_database(self, context: Context):
        '''Updates cached GTFS data for the given system'''
        print(f'Updating database with GTFS data for {context}')
        
        repositories.departure.delete_all(context)
        repositories.trip.delete_all(context)
        repositories.stop.delete_all(context)
        repositories.route.delete_all(context)
        repositories.point.delete_all(context)
        
        apply_csv(context, 'routes', repositories.route.create)
        apply_csv(context, 'stops', repositories.stop.create)
        apply_csv(context, 'trips', repositories.trip.create)
        apply_csv(context, 'stop_times', repositories.departure.create)
        apply_csv(context, 'shapes', repositories.point.create)
        
        self.database.commit()
    
    def validate(self, context: Context):
        '''Checks that the GTFS for the given context is up-to-date'''
        if not context.system.gtfs_enabled:
            return True
        if not context.system.gtfs_downloaded:
            return False
        end_dates = [s.schedule.date_range.end for s in context.system.get_services()]
        if end_dates:
            return Date.today(context.timezone) < max(end_dates) - timedelta(days=7)
        return True
    
    def update_cache(self, context: Context):
        '''Updates cached data for the given context'''
        if self.settings.update_cache_in_background:
            thread = Thread(target=context.system.update_cache)
            thread.start()
        else:
            context.system.update_cache()

def read_csv(context: Context, name, initializer):
    '''Opens a CSV file and applies an initializer to each row'''
    with open(f'./data/gtfs/{context.system_id}/{name}.txt', 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        columns = next(reader)
        return [initializer(dict(zip(columns, row))) for row in reader]

def apply_csv(context: Context, name, function):
    '''Opens a CSV file and applies a function to each row'''
    with open(f'./data/gtfs/{context.system_id}/{name}.txt', 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            function(context, dict(zip(columns, row)))

def combine_sheets(context: Context, services):
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
                sheets[-1] = Sheet(context.system, new_services, date_range)
            else:
                sheets.append(Sheet(context.system, date_range_services, date_range))
        else:
            sheets.append(Sheet(context.system, date_range_services, date_range))
    final_sheets = []
    for sheet in sheets:
        if final_sheets:
            previous_sheet = final_sheets[-1]
            if len(previous_sheet.schedule.date_range) <= 7 or len(sheet.schedule.date_range) <= 7:
                date_range = DateRange.combine([previous_sheet.schedule.date_range, sheet.schedule.date_range])
                combined_services = previous_sheet.services.union(sheet.services)
                final_sheets[-1] = Sheet(context.system, combined_services, date_range)
            else:
                final_sheets.append(sheet)
        else:
            final_sheets.append(sheet)
    return final_sheets
