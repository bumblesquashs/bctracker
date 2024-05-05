
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.assignment import Assignment

class AssignmentRepository:
    def create(self, system, block, bus, date): pass
    def find(self, system, block) -> Assignment | None: pass
    def find_all(self, system, block, bus, trip, route, stop) -> list[Assignment]: pass
    def delete_all(self, system, block, bus): pass
