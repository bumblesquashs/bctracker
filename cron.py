import os
import sys
import signal
from datetime import datetime
from crontab import CronTab

from models.system import get_systems
import gtfs
import realtime
import history
import database

PID = os.getpid()
CWD = os.path.dirname(__file__)
EXC = sys.executable
CRON_ID = f'bctracker-muncher-{PID}'

def start():
    signal.signal(signal.SIGUSR1, handle_gtfs)
    signal.signal(signal.SIGUSR2, handle_realtime)
    with CronTab(user=True) as cron:
        cron.remove_all(comment=CRON_ID)
        
        gtfs_job = cron.new(command=f'kill -s USR1 {PID}', comment=CRON_ID)
        gtfs_job.setall('0 7 */1 * *')
        
        realtime_job = cron.new(command=f'kill -s USR2 {PID}', comment=CRON_ID)
        realtime_job.minute.every(1)
        
        backup_job = cron.new(command=f'{EXC} {CWD}/backup.py', comment=CRON_ID)
        backup_job.month.every(1)

def stop():
    with CronTab(user=True) as cron:
        cron.remove_all(comment=CRON_ID)

def handle_gtfs(sig, frame):
    weekday = datetime.today().weekday()
    for system in get_systems():
        try:
            if weekday == 0 or not gtfs.validate(system):
                gtfs.update(system)
        except Exception as e:
            print(f'Error: Failed to update gtfs for {system}')
            print(f'Error message: {e}')

def handle_realtime(sig, frame):
    for system in get_systems():
        try:
            realtime.reset_positions(system)
            realtime.update(system)
            if not realtime.validate(system):
                system.realtime_validation_error_count += 1
                if system.realtime_validation_error_count <= 10 and system.realtime_validation_error_count % 2 == 0:
                    gtfs.update(system)
            else:
                system.realtime_validation_error_count = 0
        except Exception as e:
            print(f'Error: Failed to update realtime for {system}')
            print(f'Error message: {e}')
    history.update(realtime.get_positions())
    
    # Backup database at the end of each day
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
        database.backup()
