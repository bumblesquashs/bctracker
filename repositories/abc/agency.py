
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

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
    def find_all(self, enabled_only: bool = True) -> list[Agency]:
        raise NotImplementedError()
