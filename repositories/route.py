
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.route import Route

class RouteRepository:
    def create(self, system, row): pass
    def find(self, system, route_id, number) -> Route | None: pass
    def find_all(self, system, limit) -> list[Route]: pass
    def delete_all(self, system): pass
