#!/usr/bin/env python

import signal
from argparse import ArgumentParser

from di import di

from config import Config
from database import Database
from realtime import Realtime
from server import Server

from services.adornment import AdornmentService
from services.agency import AgencyService
from services.assignment import AssignmentService
from services.date import DateService
from services.departure import DepartureService
from services.model import ModelService
from services.order import OrderService
from services.overview import OverviewService
from services.point import PointService
from services.position import PositionService
from services.record import RecordService
from services.region import RegionService
from services.route import RouteService
from services.sheet import SheetService
from services.stop import StopService
from services.system import SystemService
from services.theme import ThemeService
from services.transfer import TransferService
from services.trip import TripService

def exit(sig, frame):
    server = di[Server]
    server.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit)
    
    parser = ArgumentParser()
    parser.add_argument('--reload', '-r', action='store_true', help='Re-download all GTFS data')
    parser.add_argument('--updatedb', '-u', action='store_true', help='Updates GTFS in the database with CSV data')
    parser.add_argument('--debug', '-d', action='store_true', help='Prevent page caching and show additional error info')
    
    di.add(Config())
    di.add(Database())
    di.add(Realtime())
    
    di.add(AgencyService())
    di.add(AdornmentService())
    
    server = Server()
    di.add(server)
    server.start(parser.parse_args())
