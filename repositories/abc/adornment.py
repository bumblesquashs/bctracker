
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.adornment import Adornment

class AdornmentRepository(ABC):
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, bus) -> Adornment | None:
        raise NotImplementedError()
