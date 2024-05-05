
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.departure import Departure

class DepartureRepository:
    def create(self, system, row): pass
    def find(self, system, trip, sequence, stop) -> Departure | None: pass
    def find_all(self, system, trip, sequence, route, stop, block, limit) -> list[Departure]: pass
    def find_upcoming(self, system, trip, sequence, limit) -> list[Departure]: pass
    def find_adjacent(self, system, stop) -> list[Departure]: pass
    def delete_all(self, system): pass
