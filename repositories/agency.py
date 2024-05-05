
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.agency import Agency

class AgencyRepository:
    def load(self): pass
    def find(self, agency_id) -> Agency | None: pass
    def find_all(self) -> list[Agency]: pass
