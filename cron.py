import os
import sys
import signal
from datetime import datetime, timedelta
from crontab import CronTab

import helpers.system

from models.date import Date, Weekday

import gtfs
import realtime
import database
import backup

PID = os.getpid()
CWD = os.path.dirname(__file__)
EXC = sys.executable

def setup():
    '''Adds signal handlers'''
    signal.signal(signal.SIGUSR1, handle_gtfs)
    signal.signal(signal.SIGUSR2, handle_realtime)

def start(cron_id):
    '''Removes any old cron jobs and creates new jobs'''
    with CronTab(user=True) as cron:
        cron.remove_all(comment=cron_id)
        
        gtfs_job = cron.new(command=f'kill -s USR1 {PID}', comment=cron_id)
        gtfs_job.setall('0 5 * * */1')
        
        realtime_job = cron.new(command=f'kill -s USR2 {PID}', comment=cron_id)
        realtime_job.minute.every(1)

def stop(cron_id):
    '''Removes all cron jobs'''
    with CronTab(user=True) as cron:
        cron.remove_all(comment=cron_id)

def handle_gtfs(sig, frame):
    '''Reloads GTFS every Monday, or for any system where the current GTFS is no longer valid'''
    for system in helpers.system.find_all():
        today = Date.today(system.timezone)
        try:
            if today.weekday == Weekday.MON or not gtfs.validate(system):
                gtfs.update(system)
            else:
                new_services = [s for s in system.get_services() if s.schedule.start_date == today]
                if len(new_services) > 0:
                    gtfs.load(system)
        except Exception as e:
            print(f'Error: Failed to update gtfs for {system}')
            print(f'Error message: {e}')
    date = datetime.now() - timedelta(days=1)
    backup.run(date, date.weekday() == 0)

def handle_realtime(sig, frame):
    '''Reloads realtime data for every system, and backs up data at midnight'''
    for system in helpers.system.find_all():
        try:
            realtime.update(system)
            if realtime.validate(system):
                system.validation_errors = 0
            else:
                system.validation_errors += 1
                if system.validation_errors <= 10 and system.validation_errors % 2 == 0:
                    gtfs.update(system)
        except Exception as e:
            print(f'Error: Failed to update realtime for {system}')
            print(f'Error message: {e}')
    realtime.update_records()
    
    # Backup database at the end of each day
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
        database.backup()
