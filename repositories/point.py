
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.point import Point

class PointRepository(ABC):
    
    @abstractmethod
    def create(self, system, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, shape) -> list[Point]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, system):
        raise NotImplementedError()
