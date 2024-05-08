
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.assignment import Assignment

class AssignmentRepository(ABC):
    
    @abstractmethod
    def create(self, system, block, bus, date):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, system, block) -> Assignment | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, block, bus, trip, route, stop) -> list[Assignment]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, system, block, bus):
        raise NotImplementedError()
