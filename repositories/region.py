
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.region import Region

class RegionRepository(ABC):
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, region_id) -> Region | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self) -> list[Region]:
        raise NotImplementedError()
