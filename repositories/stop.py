
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.stop import Stop

class StopRepository:
    def create(self, system, row): pass
    def find(self, system, stop_id, number) -> Stop | None: pass
    def find_all(self, system, limit) -> list[Stop]: pass
    def delete_all(self, system): pass
