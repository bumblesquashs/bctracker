import os
import signal
from crontab import CronTab

from di import di
from config import Config
from database import Database

from models.date import Date
from models.time import Time
from models.weekday import Weekday

from repositories import RecordRepository, SystemRepository
from services import BackupService, CronService, GTFSService, RealtimeService

class DefaultCronService(CronService):
    
    __slots__ = (
        'config',
        'database',
        'backup_service',
        'gtfs_service',
        'realtime_service',
        'record_repository',
        'system_repository',
        'running',
        'updating_realtime'
    )
    
    def __init__(self, **kwargs):
        self.config = kwargs.get('config') or di[Config]
        self.database = kwargs.get('database') or di[Database]
        self.backup_service = kwargs.get('backup_service') or di[BackupService]
        self.gtfs_service = kwargs.get('gtfs_service') or di[GTFSService]
        self.realtime_service = kwargs.get('realtime_service') or di[RealtimeService]
        self.record_repository = kwargs.get('record_repository') or di[RecordRepository]
        self.system_repository = kwargs.get('system_repository') or di[SystemRepository]
        self.running = True
        self.updating_realtime = False
        signal.signal(signal.SIGUSR1, lambda sig, frame: self.handle_gtfs())
        signal.signal(signal.SIGUSR2, lambda sig, frame: self.handle_realtime())
    
    def start(self):
        '''Removes any old cron jobs and creates new jobs'''
        self.running = True
        pid = os.getpid()
        with CronTab(user=True) as cron:
            cron.remove_all(comment=self.config.cron_id)
            
            gtfs_job = cron.new(command=f'kill -s USR1 {pid}', comment=self.config.cron_id)
            gtfs_job.setall('0 4 * * */1')
            
            realtime_job = cron.new(command=f'kill -s USR2 {pid}', comment=self.config.cron_id)
            realtime_job.minute.every(1)
    
    def stop(self):
        '''Removes all cron jobs'''
        self.running = False
        with CronTab(user=True) as cron:
            cron.remove_all(comment=self.config.cron_id)
    
    def handle_gtfs(self):
        '''Reloads GTFS every Monday, or for any system where the current GTFS is no longer valid'''
        for system in self.system_repository.find_all():
            if self.running:
                date = Date.today(system.timezone)
                if date.weekday == Weekday.MON or not self.gtfs_service.validate(system):
                    self.gtfs_service.load(system, True)
                    self.gtfs_service.update_cache_in_background(system)
        if self.running:
            self.record_repository.delete_stale_trip_records()
            self.database.archive()
            date = Date.today()
            self.backup_service.run(date.previous(), include_db=date.weekday == Weekday.MON)
    
    def handle_realtime(self):
        '''Reloads realtime data for every system, and backs up data at midnight'''
        if self.updating_realtime:
            return
        self.updating_realtime = True
        date = Date.today()
        time = Time.now()
        print(f'--- {date} at {time} ---')
        for system in self.system_repository.find_all():
            if self.running:
                self.realtime_service.update(system)
                if self.realtime_service.validate(system):
                    system.validation_errors = 0
                else:
                    system.validation_errors += 1
                    if system.validation_errors <= 10 and system.validation_errors % 2 == 0:
                        self.gtfs_service.load(system, True)
                        self.gtfs_service.update_cache_in_background(system)
        if self.running:
            self.realtime_service.update_records()
        self.updating_realtime = False
