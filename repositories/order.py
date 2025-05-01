
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
    def find(self, context, bus) -> Order | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context) -> list[Order]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_matches(self, context, query, recorded_bus_numbers) -> list[Match]:
        raise NotImplementedError()
