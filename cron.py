import os
import signal
from crontab import CronTab

import helpers.record
import helpers.system

from models.date import Date
from models.time import Time
from models.weekday import Weekday

import config
import gtfs
import realtime
import database
import backup

running = True
updating_realtime = False

def setup():
    '''Adds signal handlers'''
    signal.signal(signal.SIGUSR1, handle_gtfs)
    signal.signal(signal.SIGUSR2, handle_realtime)

def start():
    '''Removes any old cron jobs and creates new jobs'''
    global running
    running = True
    pid = os.getpid()
    with CronTab(user=True) as cron:
        cron.remove_all(comment=config.cron_id)
        
        gtfs_job = cron.new(command=f'kill -s USR1 {pid}', comment=config.cron_id)
        gtfs_job.setall('0 4 * * */1')
        
        realtime_job = cron.new(command=f'kill -s USR2 {pid}', comment=config.cron_id)
        realtime_job.minute.every(1)

def stop():
    '''Removes all cron jobs'''
    global running
    running = False
    with CronTab(user=True) as cron:
        cron.remove_all(comment=config.cron_id)

def handle_gtfs(sig, frame):
    '''Reloads GTFS every Monday, or for any system where the current GTFS is no longer valid'''
    for system in helpers.system.find_all():
        if running:
            date = Date.today(system.timezone)
            if date.weekday == Weekday.MON or not gtfs.validate(system):
                gtfs.load(system, True)
                gtfs.update_cache_in_background(system)
    if running:
        helpers.record.delete_stale_trip_records()
        database.archive()
        date = Date.today()
        backup.run(date.previous(), include_db=date.weekday == Weekday.MON)

def handle_realtime(sig, frame):
    '''Reloads realtime data for every system, and backs up data at midnight'''
    global updating_realtime
    if updating_realtime:
        return
    updating_realtime = True
    date = Date.today()
    time = Time.now()
    print(f'--- {date} at {time} ---')
    for system in helpers.system.find_all():
        if running:
            realtime.update(system)
            if realtime.validate(system):
                system.validation_errors = 0
            else:
                system.validation_errors += 1
                if system.validation_errors <= 10 and system.validation_errors % 2 == 0:
                    gtfs.load(system, True)
                    gtfs.update_cache_in_background(system)
    if running:
        realtime.update_records()
    updating_realtime = False
