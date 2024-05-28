#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from di import di
from database import Database
from settings import Settings
from server import Server

from repositories import *
from repositories.file import *
from repositories.sql import *

from services import *
from services.default import *

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    database = Database()
    settings = Settings()
    
    di[AdornmentRepository] = FileAdornmentRepository()
    di[AgencyRepository] = FileAgencyRepository()
    di[ModelRepository] = FileModelRepository()
    di[OrderRepository] = FileOrderRepository()
    di[RegionRepository] = FileRegionRepository()
    di[SystemRepository] = FileSystemRepository()
    di[ThemeRepository] = FileThemeRepository()
    
    di[AssignmentRepository] = SQLAssignmentRepository(database)
    di[DepartureRepository] = SQLDepartureRepository(database)
    di[OverviewRepository] = SQLOverviewRepository(database)
    di[PointRepository] = SQLPointRepository(database)
    di[PositionRepository] = SQLPositionRepository(database)
    di[RecordRepository] = SQLRecordRepository(database)
    di[RouteRepository] = SQLRouteRepository(database)
    di[StopRepository] = SQLStopRepository(database)
    di[TransferRepository] = SQLTransferRepository(database)
    di[TripRepository] = SQLTripRepository(database)
    
    di[BackupService] = DefaultBackupService(database, settings)
    di[GTFSService] = DefaultGTFSService(settings)
    di[RealtimeService] = DefaultRealtimeService(database, settings)
    di[CronService] = DefaultCronService(database, settings)
    
    server = Server(database, settings)
    
    def exit(sig, frame):
        server.stop()
    
    signal.signal(signal.SIGINT, exit)
    
    server.start(parser.parse_args())
