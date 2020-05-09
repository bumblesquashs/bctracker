#this script performs a munch - it should get called by schedule_relationship
from crontab import CronTab
import os
import realtime as rt
import scrape_fleetnums as scrape
CRON_ID_STR = 'vgtfs-muncher'
cron_interval_mins = 10

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
    print('MUNCHER: Munching!')
    rt.download_lastest_files()
    scrape.scrape()
    rt.setup_fleetnums()
    valid = rt.load_realtime()
    if(valid):
        rt.update_last_seen()
