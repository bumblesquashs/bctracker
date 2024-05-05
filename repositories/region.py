
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.region import Region

class RegionRepository:
    def load(self): pass
    def find(self, region_id) -> Region | None: pass
    def find_all(self) -> list[Region]: pass
