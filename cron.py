import os
import sys
import signal
from datetime import datetime, timedelta
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
        gtfs_job.setall('0 5 * * */1')
        
        realtime_job = cron.new(command=f'kill -s USR2 {PID}', comment=CRON_ID)
        realtime_job.minute.every(1)
        
        backup_job = cron.new(command=f'{EXC} {CWD}/backup.py', comment=CRON_ID)
        backup_job.setall('0 0 1 * *')

def stop():
    with CronTab(user=True) as cron:
        cron.remove_all(comment=CRON_ID)

def handle_gtfs(sig, frame):
    hour = datetime.now().hour
    today = datetime.today()
    date = (today if hour >= 4 else today - timedelta(days=1)).date()
    for system in get_systems():
        try:
            if date.weekday() == 0 or not gtfs.validate(system):
                gtfs.update(system)
            else:
                new_services = [s for s in system.get_services() if s.start_date == date]
                if len(new_services) > 0:
                    gtfs.load(system)
        except Exception as e:
            print(f'Error: Failed to update gtfs for {system}')
            print(f'Error message: {e}')

def handle_realtime(sig, frame):
    for system in get_systems():
        try:
            realtime.update(system)
        except Exception as e:
            print(f'Error: Failed to update realtime for {system}')
            print(f'Error message: {e}')
    history.update(realtime.get_positions())
    
    # Backup database at the end of each day
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
        database.backup()
