#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from database import Database
from settings import Settings
from server import Server

import repositories
from repositories.file import *
from repositories.sql import *

import services
from services.default import *

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    database = Database()
    settings = Settings()
    
    repositories.adornment = FileAdornmentRepository()
    repositories.agency = FileAgencyRepository()
    repositories.model = FileModelRepository()
    repositories.order = FileOrderRepository()
    repositories.region = FileRegionRepository()
    repositories.system = FileSystemRepository()
    repositories.theme = FileThemeRepository()
    
    repositories.assignment = SQLAssignmentRepository(database)
    repositories.departure = SQLDepartureRepository(database)
    repositories.overview = SQLOverviewRepository(database)
    repositories.point = SQLPointRepository(database)
    repositories.position = SQLPositionRepository(database)
    repositories.record = SQLRecordRepository(database)
    repositories.route = SQLRouteRepository(database)
    repositories.stop = SQLStopRepository(database)
    repositories.transfer = SQLTransferRepository(database)
    repositories.trip = SQLTripRepository(database)
    
    services.backup = DefaultBackupService(database, settings)
    services.gtfs = DefaultGTFSService(database, settings)
    services.realtime = DefaultRealtimeService(database, settings)
    services.cron = DefaultCronService(database, settings)
    
    server = Server(database, settings)
    
    def exit(sig, frame):
        server.stop()
    
    signal.signal(signal.SIGINT, exit)
    
    server.start(parser.parse_args())
