
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.point import Point

class PointRepository(ABC):
    
    @abstractmethod
    def create(self, context, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context, shape) -> list[Point]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, context):
        raise NotImplementedError()
