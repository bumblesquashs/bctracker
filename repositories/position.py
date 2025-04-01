
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.position import Position

class PositionRepository(ABC):
    
    @abstractmethod
    def create(self, system, agency, bus, data):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, agency, bus) -> Position | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, agency, system, trip, stop, block, route, has_location) -> list[Position]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, system):
        raise NotImplementedError()
