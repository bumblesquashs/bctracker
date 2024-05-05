
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

class SystemRepository:
    def load(self): pass
    def find(self, system_id) -> System | None: pass
    def find_all(self) -> list[System]: pass
