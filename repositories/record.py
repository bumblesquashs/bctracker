
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.bus import Bus
    from models.record import Record

class RecordRepository:
    def create(self, bus, date, system, block, time, trip) -> int: pass
    def create_trip(self, record, trip): pass
    def update(self, record, time): pass
    def find_all(self, system, bus, block, trip, limit) -> list[Record]: pass
    def find_trip_ids(self, record) -> list[str]: pass
    def find_recorded_today(self, system, trips) -> dict[str, Bus]: pass
    def delete_stale_trip_records(self): pass
