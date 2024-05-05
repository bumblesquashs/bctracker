
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.match import Match
    from models.order import Order

class OrderRepository:
    def load(self): pass
    def find(self, agency, bus) -> Order | None: pass
    def find_all(self, agency) -> list[Order]: pass
    def find_matches(self, agency, query, recorded_bus_numbers) -> list[Match]: pass
