#!/usr/bin/env python

import sys
import signal

import cron
import server

def exit(sig, frame):
    print('\n')
    cron.stop()
    server.stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    
    server.start()
    cron.start()
