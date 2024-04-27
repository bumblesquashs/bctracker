
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlite3 import Cursor
    from models.adornment import Adornment
    from models.agency import Agency
    from models.assignment import Assignment
    from models.bus import Bus
    from models.departure import Departure
    from models.match import Match
    from models.model import Model
    from models.order import Order
    from models.overview import Overview
    from models.point import Point
    from models.position import Position
    from models.record import Record
    from models.region import Region
    from models.route import Route
    from models.sheet import Sheet
    from models.stop import Stop
    from models.system import System
    from models.theme import Theme
    from models.transfer import Transfer
    from models.trip import Trip

class Config:
    def setup(self, config): pass

class Database:
    def connect(self, foreign_keys): pass
    def disconnect(self): pass
    def archive(self): pass
    def commit(self): pass
    def execute(self, sql, args) -> Cursor | None: pass
    def select(self, table, columns, distinct, ctes, join_type, joins, filters, operation, group_by, order_by, limit, page, custom_args, initializer) -> list: pass
    def insert(self, table, values) -> int | None: pass
    def update(self, table, values, filters, operation) -> Cursor | None: pass
    def delete(self, table, filters, operation) -> Cursor | None: pass
    def build_select(self, table, columns, distinct, ctes, join_type, joins, filters, operation, group_by, order_by, limit, page, custom_args) -> tuple[str, list]: pass
    def build_ctes(self, ctes) -> list[str]: pass
    def build_joins(self, joins) -> list[str]: pass
    def build_where(self, filters, operation) -> tuple[str | None, list]: pass

class AdornmentService:
    def load(self): pass
    def find(self, agency, bus) -> Adornment | None: pass

class AgencyService:
    def load(self): pass
    def find(self, agency_id) -> Agency | None: pass
    def find_all(self) -> list[Agency]: pass

class AssignmentService:
    def create(self, system, block, bus, date): pass
    def find(self, system, block) -> Assignment | None: pass
    def find_all(self, system, block, bus, trip, route, stop) -> list[Assignment]: pass
    def delete_all(self, system, block, bus): pass

class CronService:
    def start(self): pass
    def stop(self): pass
    def handle_gtfs(self): pass
    def handle_realtime(self): pass

class DateService:
    def flatten(self, dates) -> str: pass
    def days_between(self, start_date, end_date) -> int: pass

class DepartureService:
    def create(self, system, row): pass
    def find(self, system, trip, sequence, stop) -> Departure | None: pass
    def find_all(self, system, trip, sequence, route, stop, block, limit) -> list[Departure]: pass
    def find_upcoming(self, system, trip, sequence, limit) -> list[Departure]: pass
    def find_adjacent(self, system, stop) -> list[Departure]: pass
    def delete_all(self, system): pass

class GTFSService:
    def load(self, system, force_download, update_db): pass
    def download(self, system): pass
    def update_database(self, system): pass
    def validate(self, system) -> bool: pass
    def update_cache_in_background(self, system): pass

class ModelService:
    def load(self): pass
    def find(self, model_id) -> Model | None: pass

class OrderService:
    def load(self): pass
    def find(self, agency, bus) -> Order | None: pass
    def find_all(self, agency) -> list[Order]: pass
    def find_matches(self, agency, query, recorded_bus_numbers) -> list[Match]: pass

class OverviewService:
    def create(self, bus, date, system, record): pass
    def find(self, bus) -> Overview | None: pass
    def find_all(self, system, last_seen_system, bus, limit) -> list[Overview]: pass
    def find_bus_numbers(self, system) -> list[int]: pass
    def update(self, overview, date, system, record): pass

class PointService:
    def create(self, system, row): pass
    def find_all(self, system, shape) -> list[Point]: pass
    def delete_all(self, system): pass

class PositionService:
    def create(self, system, bus, data): pass
    def find(self, bus) -> Position | None: pass
    def find_all(self, system, trip, stop, block, route, has_location) -> list[Position]: pass
    def delete_all(self, system): pass

class RealtimeService:
    def update(self, system): pass
    def update_records(self): pass
    def get_last_updated(self, time_format) -> str | None: pass
    def validate(self, system) -> bool: pass

class RecordService:
    def create(self, bus, date, system, block, time, trip) -> int: pass
    def create_trip(self, record, trip): pass
    def update(self, record, time): pass
    def find_all(self, system, bus, block, trip, limit) -> list[Record]: pass
    def find_trip_ids(self, record) -> list[str]: pass
    def find_recorded_today(self, system, trips) -> dict[str, Bus]: pass
    def delete_stale_trip_records(self): pass

class RegionService:
    def load(self): pass
    def find(self, region_id) -> Region | None: pass
    def find_all(self) -> list[Region]: pass

class RouteService:
    def create(self, system, row): pass
    def find(self, system, route_id, number) -> Route | None: pass
    def find_all(self, system, limit) -> list[Route]: pass
    def delete_all(self, system): pass

class SheetService:
    def combine(self, system, services) -> list[Sheet]: pass

class StopService:
    def create(self, system, row): pass
    def find(self, system, stop_id, number) -> Stop | None: pass
    def find_all(self, system, limit) -> list[Stop]: pass
    def delete_all(self, system): pass

class SystemService:
    def load(self): pass
    def find(self, system_id) -> System | None: pass
    def find_all(self) -> list[System]: pass

class ThemeService:
    def load(self): pass
    def find(self, theme_id) -> Theme | None: pass
    def find_all(self) -> list[Theme]: pass

class TransferService:
    def create(self, bus, date, old_system, new_system): pass
    def find_all(self, old_system, new_system, bus, limit) -> list[Transfer]: pass

class TripService:
    def create(self, system, row): pass
    def find(self, system, trip_id) -> Trip | None: pass
    def find_all(self, system, route, block, limit) -> list[Trip]: pass
    def delete_all(self, system): pass
