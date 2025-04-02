
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.match import Match
    from models.order import Order

class OrderRepository(ABC):
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, agency, bus) -> Order | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, agency) -> list[Order]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_matches(self, system, agency, query, recorded_bus_numbers) -> list[Match]:
        raise NotImplementedError()
