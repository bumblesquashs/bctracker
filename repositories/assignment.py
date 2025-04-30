
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.assignment import Assignment

class AssignmentRepository(ABC):
    
    @abstractmethod
    def create(self, context, block, bus, date):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, context, block) -> Assignment | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context, block, bus, trip, route, stop) -> list[Assignment]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, context, block, bus):
        raise NotImplementedError()
