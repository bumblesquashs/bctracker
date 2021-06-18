import os
import time
import signal
from crontab import CronTab

from models.system import all_systems
from models.realtime import get_realtime

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
    try:
        get_realtime().reset_realtime_positions()
        for system in all_systems():
            try:
                system.update_realtime()
                if not system.validate_gtfs():
                    system.update_gtfs()
            except Exception as e:
                print(f'Error: Hit exception loading realtime for system: {system.name}')
                print(f'Error message: {e}')
        get_realtime().last_updated_time = time.time()
    except Exception as e:
        # We should not let any python exceptions propogate out of a signal handler
        print('Error: Hit exception in cron signal handler')
        print(f'Error message: {e}')
    return
