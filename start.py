#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from database import Database
from settings import Settings
from server import Server

import repositories
import services

from repositories.impl import *
from services.impl import *

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    database = Database()
    settings = Settings()
    
    repositories.agency = AgencyRepository()
    repositories.decoration = DecorationRepository()
    repositories.livery = LiveryRepository()
    repositories.model = ModelRepository()
    repositories.order = OrderRepository()
    repositories.region = RegionRepository()
    repositories.system = SystemRepository()
    repositories.theme = ThemeRepository()
    
    repositories.allocation = AllocationRepository(database)
    repositories.assignment = AssignmentRepository(database)
    repositories.departure = DepartureRepository(database)
    repositories.point = PointRepository(database)
    repositories.position = PositionRepository(database)
    repositories.record = RecordRepository(database)
    repositories.route = RouteRepository(database)
    repositories.stop = StopRepository(database)
    repositories.transfer = TransferRepository(database)
    repositories.trip = TripRepository(database)
    
    services.log = LogService()
    services.backup = BackupService(database, settings)
    services.gtfs = GTFSService(database, settings)
    services.realtime = RealtimeService(database, settings)
    services.cron = CronService(database, settings)
    
    server = Server(database, settings)
    
    def exit(sig, frame):
        server.stop()
    
    signal.signal(signal.SIGINT, exit)
    
    server.start(parser.parse_args())
