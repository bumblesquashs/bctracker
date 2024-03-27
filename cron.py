import os
import signal
from crontab import CronTab

from models.date import Date
from models.time import Time
from models.weekday import Weekday

import gtfs
import realtime
import backup

from di import di

from config import Config
from database import Database
from server import Server

from services.record import RecordService
from services.system import SystemService

class Cron:
    
    __slots__ = (
        'config',
        'database',
        'server',
        'record_service',
        'system_service'
    )
    
    def __init__(self):
        self.config = di[Config]
        self.database = di[Database]
        self.server = di[Server]
        self.record_service = di[RecordService]
        self.system_service = di[SystemService]
        
        signal.signal(signal.SIGUSR1, self.handle_gtfs)
        signal.signal(signal.SIGUSR2, self.handle_realtime)
    
    def start(self):
        '''Removes any old cron jobs and creates new jobs'''
        pid = os.getpid()
        with CronTab(user=True) as cron:
            cron.remove_all(comment=self.config.cron_id)
            
            gtfs_job = cron.new(command=f'kill -s USR1 {pid}', comment=self.config.cron_id)
            gtfs_job.setall('0 4 * * */1')
            
            realtime_job = cron.new(command=f'kill -s USR2 {pid}', comment=self.config.cron_id)
            realtime_job.minute.every(1)
    
    def stop(self):
        '''Removes all cron jobs'''
        with CronTab(user=True) as cron:
            cron.remove_all(comment=self.config.cron_id)
    
    def handle_gtfs(self, sig, frame):
        '''Reloads GTFS every Monday, or for any system where the current GTFS is no longer valid'''
        for system in self.system_service.find_all():
            if self.server.running:
                date = Date.today(system.timezone)
                if date.weekday == Weekday.MON or not gtfs.validate(system):
                    gtfs.load(system, True)
                    gtfs.update_cache_in_background(system)
        if self.server.running:
            self.record_service.delete_stale_trip_records()
            self.database.archive()
            date = Date.today()
            backup.run(date.previous(), include_db=date.weekday == Weekday.MON)
    
    def handle_realtime(self, sig, frame):
        '''Reloads realtime data for every system, and backs up data at midnight'''
        date = Date.today()
        time = Time.now()
        print(f'--- {date} at {time} ---')
        for system in self.system_service.find_all():
            if self.server.running:
                realtime.update(system)
                if realtime.validate(system):
                    system.validation_errors = 0
                else:
                    system.validation_errors += 1
                    if system.validation_errors <= 10 and system.validation_errors % 2 == 0:
                        gtfs.load(system, True)
                        gtfs.update_cache_in_background(system)
        if self.server.running:
            realtime.update_records()
