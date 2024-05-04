#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from di import di

from repositories import *
from services import *

from config import Config
from database import Database

from repositories.adornment import DefaultAdornmentRepository
from repositories.agency import DefaultAgencyRepository
from repositories.assignment import DefaultAssignmentRepository
from repositories.departure import DefaultDepartureRepository
from repositories.model import DefaultModelRepository
from repositories.order import DefaultOrderRepository
from repositories.overview import DefaultOverviewRepository
from repositories.point import DefaultPointRepository
from repositories.position import DefaultPositionRepository
from repositories.record import DefaultRecordRepository
from repositories.region import DefaultRegionRepository
from repositories.route import DefaultRouteRepository
from repositories.stop import DefaultStopRepository
from repositories.system import DefaultSystemRepository
from repositories.theme import DefaultThemeRepository
from repositories.transfer import DefaultTransferRepository
from repositories.trip import DefaultTripRepository

from services.backup import DefaultBackupService
from services.cron import DefaultCronService
from services.gtfs import DefaultGTFSService
from services.realtime import DefaultRealtimeService

from server import Server

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    di[Config] = Config()
    di[Database] = Database()
    
    di[AdornmentRepository] = DefaultAdornmentRepository()
    di[AgencyRepository] = DefaultAgencyRepository()
    di[ModelRepository] = DefaultModelRepository()
    di[OrderRepository] = DefaultOrderRepository()
    di[RegionRepository] = DefaultRegionRepository()
    di[SystemRepository] = DefaultSystemRepository()
    di[ThemeRepository] = DefaultThemeRepository()
    
    di[AssignmentRepository] = DefaultAssignmentRepository()
    di[DepartureRepository] = DefaultDepartureRepository()
    di[OverviewRepository] = DefaultOverviewRepository()
    di[PointRepository] = DefaultPointRepository()
    di[PositionRepository] = DefaultPositionRepository()
    di[RecordRepository] = DefaultRecordRepository()
    di[RouteRepository] = DefaultRouteRepository()
    di[StopRepository] = DefaultStopRepository()
    di[TransferRepository] = DefaultTransferRepository()
    di[TripRepository] = DefaultTripRepository()
    
    di[BackupService] = DefaultBackupService()
    di[GTFSService] = DefaultGTFSService()
    di[RealtimeService] = DefaultRealtimeService()
    di[CronService] = DefaultCronService()
    
    server = Server()
    
    def exit(sig, frame):
        server.stop()
    
    signal.signal(signal.SIGINT, exit)
    
    server.start(parser.parse_args())
