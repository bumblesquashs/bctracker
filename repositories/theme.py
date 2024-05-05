
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.theme import Theme

class ThemeRepository:
    def load(self): pass
    def find(self, theme_id) -> Theme | None: pass
    def find_all(self) -> list[Theme]: pass
