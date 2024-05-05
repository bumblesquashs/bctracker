
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.departure import Departure

class DepartureRepository(ABC):
    
    @abstractmethod
    def create(self, system, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, system, trip, sequence, stop) -> Departure | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, trip, sequence, route, stop, block, limit) -> list[Departure]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_upcoming(self, system, trip, sequence, limit) -> list[Departure]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_adjacent(self, system, stop) -> list[Departure]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, system):
        raise NotImplementedError()
