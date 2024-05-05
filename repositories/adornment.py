
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.adornment import Adornment

class AdornmentRepository:
    def load(self): pass
    def find(self, agency, bus) -> Adornment | None: pass
