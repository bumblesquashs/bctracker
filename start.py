#!/usr/bin/env python
# set up for linux

import sys
import signal

import cron
import server

def exit(sig, frame):
    cron.stop()
    server.stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit)
    
    cron.start()
    server.start()
