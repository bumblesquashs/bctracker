#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from di import di

from config import Config
from database import Database

def exit(sig, frame):
    # temporary inline import to avoid injection issues
    import server
    server.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    di.add(Config())
    di.add(Database())
    
    # temporary inline import to avoid injection issues
    import server
    server.start(parser.parse_args())
