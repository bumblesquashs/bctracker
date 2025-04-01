
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.transfer import Transfer

class TransferRepository(ABC):
    
    @abstractmethod
    def create(self, agency, bus, date, old_system, new_system):
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, old_system, new_system, agency, bus, limit) -> list[Transfer]:
        raise NotImplementedError()
