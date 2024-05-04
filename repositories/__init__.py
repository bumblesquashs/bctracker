
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
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
    from models.stop import Stop
    from models.system import System
    from models.theme import Theme
    from models.transfer import Transfer
    from models.trip import Trip

class AdornmentRepository:
    def load(self): pass
    def find(self, agency, bus) -> Adornment | None: pass

class AgencyRepository:
    def load(self): pass
    def find(self, agency_id) -> Agency | None: pass
    def find_all(self) -> list[Agency]: pass

class AssignmentRepository:
    def create(self, system, block, bus, date): pass
    def find(self, system, block) -> Assignment | None: pass
    def find_all(self, system, block, bus, trip, route, stop) -> list[Assignment]: pass
    def delete_all(self, system, block, bus): pass

class DepartureRepository:
    def create(self, system, row): pass
    def find(self, system, trip, sequence, stop) -> Departure | None: pass
    def find_all(self, system, trip, sequence, route, stop, block, limit) -> list[Departure]: pass
    def find_upcoming(self, system, trip, sequence, limit) -> list[Departure]: pass
    def find_adjacent(self, system, stop) -> list[Departure]: pass
    def delete_all(self, system): pass

class ModelRepository:
    def load(self): pass
    def find(self, model_id) -> Model | None: pass

class OrderRepository:
    def load(self): pass
    def find(self, agency, bus) -> Order | None: pass
    def find_all(self, agency) -> list[Order]: pass
    def find_matches(self, agency, query, recorded_bus_numbers) -> list[Match]: pass

class OverviewRepository:
    def create(self, bus, date, system, record): pass
    def find(self, bus) -> Overview | None: pass
    def find_all(self, system, last_seen_system, bus, limit) -> list[Overview]: pass
    def find_bus_numbers(self, system) -> list[int]: pass
    def update(self, overview, date, system, record): pass

class PointRepository:
    def create(self, system, row): pass
    def find_all(self, system, shape) -> list[Point]: pass
    def delete_all(self, system): pass

class PositionRepository:
    def create(self, system, bus, data): pass
    def find(self, bus) -> Position | None: pass
    def find_all(self, system, trip, stop, block, route, has_location) -> list[Position]: pass
    def delete_all(self, system): pass

class RecordRepository:
    def create(self, bus, date, system, block, time, trip) -> int: pass
    def create_trip(self, record, trip): pass
    def update(self, record, time): pass
    def find_all(self, system, bus, block, trip, limit) -> list[Record]: pass
    def find_trip_ids(self, record) -> list[str]: pass
    def find_recorded_today(self, system, trips) -> dict[str, Bus]: pass
    def delete_stale_trip_records(self): pass

class RegionRepository:
    def load(self): pass
    def find(self, region_id) -> Region | None: pass
    def find_all(self) -> list[Region]: pass

class RouteRepository:
    def create(self, system, row): pass
    def find(self, system, route_id, number) -> Route | None: pass
    def find_all(self, system, limit) -> list[Route]: pass
    def delete_all(self, system): pass

class StopRepository:
    def create(self, system, row): pass
    def find(self, system, stop_id, number) -> Stop | None: pass
    def find_all(self, system, limit) -> list[Stop]: pass
    def delete_all(self, system): pass

class SystemRepository:
    def load(self): pass
    def find(self, system_id) -> System | None: pass
    def find_all(self) -> list[System]: pass

class ThemeRepository:
    def load(self): pass
    def find(self, theme_id) -> Theme | None: pass
    def find_all(self) -> list[Theme]: pass

class TransferRepository:
    def create(self, bus, date, old_system, new_system): pass
    def find_all(self, old_system, new_system, bus, limit) -> list[Transfer]: pass

class TripRepository:
    def create(self, system, row): pass
    def find(self, system, trip_id) -> Trip | None: pass
    def find_all(self, system, route, block, limit) -> list[Trip]: pass
    def delete_all(self, system): pass
