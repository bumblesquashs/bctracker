
class Config:
    def setup(self, config): pass

class Database:
    def connect(self, foreign_keys=True): pass
    def disconnect(self): pass
    def archive(self): pass
    def commit(self): pass
    def execute(self, sql, args): pass
    def select(self, table, columns, distinct, ctes, join_type, joins, filters, operation, group_by, order_by, limit, page, custom_args, initializer): pass
    def insert(self, table, values): pass
    def update(self, table, values, filters, operation): pass
    def delete(self, table, filters, operation): pass
    def build_select(self, table, columns, distinct, ctes, join_type, joins, filters, operation, group_by, order_by, limit, page, custom_args): pass
    def build_ctes(self, ctes): pass
    def build_joins(self, joins): pass
    def build_where(self, filters, operation): pass

class AdornmentService:
    def load(self): pass
    def find(self, agency, bus): pass

class AgencyService:
    def load(self): pass
    def find(self, agency_id): pass
    def find_all(self): pass

class AssignmentService:
    def create(self, system, block, bus, date): pass
    def find(self, system, block): pass
    def find_all(self, system, block, bus, trip, route, stop): pass
    def delete_all(self, system, block, bus): pass

class CronService:
    def start(self): pass
    def stop(self): pass
    def handle_gtfs(self): pass
    def handle_realtime(self): pass

class DateService:
    def flatten(dates): pass
    def days_between(start_date, end_date): pass

class DepartureService:
    def create(self, system, row): pass
    def find(self, system, trip, sequence, stop): pass
    def find_all(self, system, trip, sequence, route, stop, block, limit): pass
    def find_upcoming(self, system, trip, sequence, limit): pass
    def find_adjacent(self, system, stop): pass
    def delete_all(self, system): pass

class GTFSService:
    def load(self, system, force_download, update_db): pass
    def download(self, system): pass
    def update_database(self, system): pass
    def validate(self, system): pass
    def update_cache_in_background(self, system): pass

class ModelService:
    def load(self): pass
    def find(self, model_id): pass

class OrderService:
    def load(self): pass
    def find(self, agency, bus): pass
    def find_all(self, agency): pass
    def find_matches(self, agency, query, recorded_bus_numbers): pass

class OverviewService:
    def create(self, bus, date, system, record): pass
    def find(self, bus): pass
    def find_all(self, system, last_seen_system, bus, limit): pass
    def find_bus_numbers(self, system): pass
    def update(self, overview, date, system, record): pass

class PointService:
    def create(self, system, row): pass
    def find_all(self, system, shape): pass
    def delete_all(self, system): pass

class PositionService:
    def create(self, system, bus, data): pass
    def find(self, bus): pass
    def find_all(self, system, trip, stop, block, route, has_location): pass
    def delete_all(self, system): pass

class RealtimeService:
    def update(self, system): pass
    def update_records(self): pass
    def get_last_updated(self, time_format): pass
    def validate(self, system): pass

class RecordService:
    def create(self, bus, date, system, block, time, trip): pass
    def create_trip(self, record, trip): pass
    def update(self, record, time): pass
    def find_all(self, system, bus, block, trip, limit): pass
    def find_trip_ids(self, record): pass
    def find_recorded_today(self, system, trips): pass
    def delete_stale_trip_records(self): pass

class RegionService:
    def load(self): pass
    def find(self, region_id): pass
    def find_all(self): pass

class RouteService:
    def create(self, system, row): pass
    def find(self, system, route_id, number): pass
    def find_all(self, system, limit): pass
    def delete_all(self, system): pass

class SheetService:
    def combine(self, system, services): pass

class StopService:
    def create(self, system, row): pass
    def find(self, system, stop_id, number): pass
    def find_all(self, system, limit): pass
    def delete_all(self, system): pass

class SystemService:
    def load(self): pass
    def find(self, system_id): pass
    def find_all(self): pass

class ThemeService:
    def load(self): pass
    def find(self, theme_id): pass
    def find_all(self): pass

class TransferService:
    def create(self, bus, date, old_system, new_system): pass
    def find_all(self, old_system, new_system, bus, limit): pass

class TripService:
    def create(self, system, row): pass
    def find(self, system, trip_id): pass
    def find_all(self, system, route, block, limit): pass
    def delete_all(self, system): pass
