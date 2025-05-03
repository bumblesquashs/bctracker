
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.overview import Overview

class OverviewRepository(ABC):
    
    @abstractmethod
    def create(self, context, bus, date, record):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, bus) -> Overview | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context, last_seen_context, bus, limit) -> list[Overview]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_bus_numbers(self, context) -> list[int]:
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, context, overview, date, record):
        raise NotImplementedError()
