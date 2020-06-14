#this script performs a munch - it should get called by schedule_relationship
from crontab import CronTab
import os
import realtime as rt
import scrape_fleetnums as scrape
import start
import history as hist

CRON_ID_STR = 'vgtfs-muncher'
cron_interval_mins = 5
munch_count = 1

def start_cron():
    with CronTab(user=True) as cron:
        cron.remove_all(comment=CRON_ID_STR)
        job = cron.new(command='kill -s USR1 {0}'.format(os.getpid()), comment=CRON_ID_STR)
        job.minute.every(cron_interval_mins)
    print('MUNCHER: cron job to munch realtime was just setup')

def stop_cron():
    with CronTab(user=True) as cron:
        cron.remove_all(comment=CRON_ID_STR)
    print('MUNCHER:  cron job to munch realtime was just removed')

#code to run under cron:
#this should get triggered every cron_interval_mins mins
def munch():
    global munch_count
    print('MUNCHER: Munching!')
    munch_count += 1
    rt.download_lastest_files()
    scrape.scrape()
    rt.setup_fleetnums()
    valid = rt.load_realtime()
    if(valid):
        hist.update_last_seen()
    if((not rt.data_valid) and (munch_count % 2 == 0)):
        print('INVALID DATA: downloading new gtfs and trying again!')
        start.download_and_restart
    return valid
