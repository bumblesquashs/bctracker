
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.stop import Stop

class StopRepository(ABC):
    
    @abstractmethod
    def create(self, system, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, system, stop_id, number) -> Stop | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, limit) -> list[Stop]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, system):
        raise NotImplementedError()
