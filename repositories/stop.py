
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.area import Area
    from models.stop import Stop

class StopRepository(ABC):
    
    @abstractmethod
    def create(self, system, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, system, stop_id, number) -> Stop | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, limit=None, lat=None, lon=None, size=0.01) -> list[Stop]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_area(self, system) -> Area:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, system):
        raise NotImplementedError()
