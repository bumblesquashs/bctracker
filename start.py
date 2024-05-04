#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from di import di

from services import *

from services.config import DefaultConfig
from services.database import DefaultDatabase

from services.adornment import DefaultAdornmentService
from services.agency import DefaultAgencyService
from services.assignment import DefaultAssignmentService
from services.backup import DefaultBackupService
from services.cron import DefaultCronService
from services.departure import DefaultDepartureService
from services.gtfs import DefaultGTFSService
from services.model import DefaultModelService
from services.order import DefaultOrderService
from services.overview import DefaultOverviewService
from services.point import DefaultPointService
from services.position import DefaultPositionService
from services.realtime import DefaultRealtimeService
from services.record import DefaultRecordService
from services.region import DefaultRegionService
from services.route import DefaultRouteService
from services.stop import DefaultStopService
from services.system import DefaultSystemService
from services.theme import DefaultThemeService
from services.transfer import DefaultTransferService
from services.trip import DefaultTripService

from server import Server

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    di[Config] = DefaultConfig()
    di[Database] = DefaultDatabase()
    
    di[AdornmentService] = DefaultAdornmentService()
    di[AgencyService] = DefaultAgencyService()
    di[ModelService] = DefaultModelService()
    di[OrderService] = DefaultOrderService()
    di[RegionService] = DefaultRegionService()
    di[SystemService] = DefaultSystemService()
    di[ThemeService] = DefaultThemeService()
    
    di[AssignmentService] = DefaultAssignmentService()
    di[DepartureService] = DefaultDepartureService()
    di[OverviewService] = DefaultOverviewService()
    di[PointService] = DefaultPointService()
    di[PositionService] = DefaultPositionService()
    di[RecordService] = DefaultRecordService()
    di[RouteService] = DefaultRouteService()
    di[StopService] = DefaultStopService()
    di[TransferService] = DefaultTransferService()
    di[TripService] = DefaultTripService()
    
    di[BackupService] = DefaultBackupService()
    di[GTFSService] = DefaultGTFSService()
    di[RealtimeService] = DefaultRealtimeService()
    di[CronService] = DefaultCronService()
    
    server = Server()
    
    def exit(sig, frame):
        server.stop()
    
    signal.signal(signal.SIGINT, exit)
    
    server.start(parser.parse_args())
