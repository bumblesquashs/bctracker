#!/usr/bin/env python

import signal
from argparse import ArgumentParser

import server

def exit(sig, frame):
    server.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    server.start(parser.parse_args())
