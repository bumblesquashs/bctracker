
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.system import System

class SystemRepository(ABC):
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, system_id) -> System | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self) -> list[System]:
        raise NotImplementedError()
