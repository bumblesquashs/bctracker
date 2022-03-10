#!/usr/bin/env python

import sys
import signal
from argparse import ArgumentParser

import cron
import server

def exit(sig, frame):
    print('\n')
    cron.stop()
    server.stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    server.start(parser.parse_args())
    cron.start()
