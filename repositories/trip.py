
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.trip import Trip

class TripRepository(ABC):
    
    @abstractmethod
    def create(self, system, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, system, trip_id) -> Trip | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, route, block, limit) -> list[Trip]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, system):
        raise NotImplementedError()
