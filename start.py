#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from di import di

import server

from config import Config
from database import Database

from helpers.adornment import AdornmentService
from helpers.agency import AgencyService
from helpers.order import OrderService
from helpers.overview import OverviewService
from helpers.model import ModelService
from helpers.region import RegionService
from helpers.system import SystemService
from helpers.theme import ThemeService

from helpers.assignment import AssignmentService
from helpers.departure import DepartureService
from helpers.point import PointService
from helpers.position import PositionService
from helpers.record import RecordService
from helpers.route import RouteService
from helpers.stop import StopService
from helpers.transfer import TransferService
from helpers.trip import TripService

from helpers.cron import CronService
from helpers.date import DateService
from helpers.gtfs import GTFSService
from helpers.realtime import RealtimeService
from helpers.sheet import SheetService

def exit(sig, frame):
    server.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    di.add(Config())
    di.add(Database())
    
    di.add(AdornmentService())
    di.add(AgencyService())
    di.add(ModelService())
    di.add(OrderService())
    di.add(RegionService())
    di.add(SystemService())
    di.add(ThemeService())
    
    di.add(AssignmentService())
    di.add(DepartureService())
    di.add(OverviewService())
    di.add(PointService())
    di.add(PositionService())
    di.add(RecordService())
    di.add(RouteService())
    di.add(StopService())
    di.add(TransferService())
    di.add(TripService())
    
    di.add(DateService())
    di.add(SheetService())
    di.add(GTFSService())
    di.add(RealtimeService())
    di.add(CronService())
    
    server.start(parser.parse_args())
