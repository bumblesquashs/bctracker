import os
import signal
from crontab import CronTab

import database
import helpers.gtfs
import helpers.realtime
import helpers.record
import helpers.system

from models.date import Date
from models.time import Time
from models.weekday import Weekday

import backup
import config

class CronService:
    
    __slots__ = (
        'running',
        'updating_realtime'
    )
    
    def __init__(self):
        self.running = True
        self.updating_realtime = False
        signal.signal(signal.SIGUSR1, lambda sig, frame: self.handle_gtfs())
        signal.signal(signal.SIGUSR2, lambda sig, frame: self.handle_realtime())
    
    def start(self):
        '''Removes any old cron jobs and creates new jobs'''
        self.running = True
        pid = os.getpid()
        with CronTab(user=True) as cron:
            cron.remove_all(comment=config.default.cron_id)
            
            gtfs_job = cron.new(command=f'kill -s USR1 {pid}', comment=config.default.cron_id)
            gtfs_job.setall('0 4 * * */1')
            
            realtime_job = cron.new(command=f'kill -s USR2 {pid}', comment=config.default.cron_id)
            realtime_job.minute.every(1)
    
    def stop(self):
        '''Removes all cron jobs'''
        self.running = False
        with CronTab(user=True) as cron:
            cron.remove_all(comment=config.default.cron_id)
    
    def handle_gtfs(self):
        '''Reloads GTFS every Monday, or for any system where the current GTFS is no longer valid'''
        for system in helpers.system.default.find_all():
            if self.running:
                date = Date.today(system.timezone)
                if date.weekday == Weekday.MON or not helpers.gtfs.default.validate(system):
                    helpers.gtfs.default.load(system, True)
                    helpers.gtfs.default.update_cache_in_background(system)
        if self.running:
            helpers.record.default.delete_stale_trip_records()
            database.archive()
            date = Date.today()
            backup.run(date.previous(), include_db=date.weekday == Weekday.MON)
    
    def handle_realtime(self):
        '''Reloads realtime data for every system, and backs up data at midnight'''
        if self.updating_realtime:
            return
        self.updating_realtime = True
        date = Date.today()
        time = Time.now()
        print(f'--- {date} at {time} ---')
        for system in helpers.system.default.find_all():
            if self.running:
                helpers.realtime.default.update(system)
                if helpers.realtime.default.validate(system):
                    system.validation_errors = 0
                else:
                    system.validation_errors += 1
                    if system.validation_errors <= 10 and system.validation_errors % 2 == 0:
                        helpers.gtfs.default.load(system, True)
                        helpers.gtfs.default.update_cache_in_background(system)
        if self.running:
            helpers.realtime.default.update_records()
        self.updating_realtime = False

default = CronService()
