
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.transfer import Transfer

class TransferRepository:
    def create(self, bus, date, old_system, new_system): pass
    def find_all(self, old_system, new_system, bus, limit) -> list[Transfer]: pass
