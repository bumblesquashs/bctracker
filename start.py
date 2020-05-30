#!/usr/bin/env python
# set up for linux

import os
import sys
import web
import munch
import signal
import inspect
import subprocess
import requestlogger
import realtime as rt
import datastructure as ds
from pages.stop import stoppage_html

#some config
AUTO_RELOAD = True
RELOAD_ENABLED = True
COMBINE_WEEKDAYS = False

def controlc_handler(sig, frame):
    print('\n')
    munch.stop_cron()
    print('EXITING: Gooodbye Everybody!')
    sys.exit(0)

def restart_server():
    print('\n')
    munch.stop_cron()
    print('RESTARTING: Loading New static GTFS!')
    os.execv(inspect.getfile(lambda: None), sys.argv)

def download_and_restart():
    print('INVALID GTFS: Automatically restarting... (or reload requested?)')
    try:
        subprocess.call(['./download_new_gtfs.sh'], timeout = 45)
    except subprocess.TimeoutExpired:
        try:
            subprocess.call(['./download_new_gtfs.sh'], timeout = 60)
        except subprocess.TimeoutExpired:
            print('WTF: timeout expired twice, guess no connection?')
            controlc_handler()
    subprocess.call(['./download_new_routes.sh'], timeout = 15)
    restart_server()
    print('this should never be seen haha!')



def crontask_handler(sig, frame):
    try:
        valid = munch.munch()
        if((not valid) and AUTO_RELOAD):
            download_and_restart()
    except:
        print('MUNCH: (in sighandler) Hit exception...')
    return

if __name__ == "__main__":
    signal.signal(signal.SIGINT, controlc_handler)
    signal.signal(signal.SIGUSR1, crontask_handler)
    ds.start()
    rt.download_lastest_files()
    valid = rt.load_realtime()
    if(not valid):
        print('ERROR: Not valid on startup... now thats a zinger.')
        print('ERROR: Try running the download new gtfs script and try again')
        print('ERROR: Going without logging...')
        rt.data_valid = False
    rt.update_last_seen()
    munch.start_cron()
    web.startup()
