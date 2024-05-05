
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.trip import Trip

class TripRepository:
    def create(self, system, row): pass
    def find(self, system, trip_id) -> Trip | None: pass
    def find_all(self, system, route, block, limit) -> list[Trip]: pass
    def delete_all(self, system): pass
