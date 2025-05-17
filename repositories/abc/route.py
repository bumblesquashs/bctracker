
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.route import Route

class RouteRepository(ABC):
    
    @abstractmethod
    def create(self, context, row):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, context, route_id, number) -> Route | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context, limit) -> list[Route]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_all(self, context):
        raise NotImplementedError()
