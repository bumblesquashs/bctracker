
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.departure import Departure

class DepartureRepository(ABC):
    
    @abstractmethod
    def create(self, context, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, context, trip, sequence, stop) -> Departure | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context, trip, sequence, route, stop, block, limit) -> list[Departure]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_upcoming(self, context, trip, sequence, limit) -> list[Departure]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_adjacent(self, context, stop) -> list[Departure]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, context):
        raise NotImplementedError()
