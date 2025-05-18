
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.area import Area
    from models.stop import Stop

class StopRepository(ABC):
    
    @abstractmethod
    def create(self, context, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, context, stop_id, number) -> Stop | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context, limit=None, lat=None, lon=None, size=0.01) -> list[Stop]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_area(self, context) -> Area:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, context):
        raise NotImplementedError()
