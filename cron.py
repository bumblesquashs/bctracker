import os
import signal
from crontab import CronTab

from models.system import all_systems
import gtfs
import realtime
import history

CRON_ID = 'gtfs-muncher'
CRON_INTERVAL = 5

def start():
    signal.signal(signal.SIGUSR1, handle)
    pid = os.getpid()
    with CronTab(user=True) as cron:
        cron.remove_all(comment=CRON_ID)
        job = cron.new(command=f'kill -s USR1 {pid}', comment=CRON_ID)
        job.minute.every(CRON_INTERVAL)

def stop():
    with CronTab(user=True) as cron:
        cron.remove_all(comment=CRON_ID)

def handle(sig, frame):
    realtime.reset_positions()
    for system in all_systems():
        try:
            realtime.update(system)
            if not gtfs.validate(system):
                gtfs.update(system)
                realtime.update_routes(system)
        except Exception as e:
            print(f'Error: Failed to update realtime for {system}')
            print(f'Error message: {e}')
    history.update(realtime.active_buses())
