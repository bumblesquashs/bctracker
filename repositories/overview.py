
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.overview import Overview

class OverviewRepository:
    def create(self, bus, date, system, record): pass
    def find(self, bus) -> Overview | None: pass
    def find_all(self, system, last_seen_system, bus, limit) -> list[Overview]: pass
    def find_bus_numbers(self, system) -> list[int]: pass
    def update(self, overview, date, system, record): pass
