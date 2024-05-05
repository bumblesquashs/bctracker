
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.position import Position

class PositionRepository:
    def create(self, system, bus, data): pass
    def find(self, bus) -> Position | None: pass
    def find_all(self, system, trip, stop, block, route, has_location) -> list[Position]: pass
    def delete_all(self, system): pass
