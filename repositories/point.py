
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.point import Point

class PointRepository:
    def create(self, system, row): pass
    def find_all(self, system, shape) -> list[Point]: pass
    def delete_all(self, system): pass
