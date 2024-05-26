
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.bus import Bus
    from models.overview import Overview

class OverviewRepository(ABC):
    
    @abstractmethod
    def create(self, bus, date, system, record):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, bus) -> Overview | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, last_seen_system, bus, limit) -> list[Overview]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_bus_numbers(self, system) -> list[int]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_yard_buses(self, system, stop) -> list[Bus]:
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, overview, date, system, record):
        raise NotImplementedError()
