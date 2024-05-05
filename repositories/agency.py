
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.agency import Agency

class AgencyRepository(ABC):
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, agency_id) -> Agency | None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self) -> list[Agency]:
        raise NotImplementedError()
