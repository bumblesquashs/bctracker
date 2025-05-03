
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.theme import Theme

class ThemeRepository(ABC):
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, theme_id) -> Theme | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self) -> list[Theme]:
        raise NotImplementedError()
