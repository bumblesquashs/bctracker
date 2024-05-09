
from __future__ import annotations
from abc import ABC, abstractmethod

class RealtimeService(ABC):
    
    @abstractmethod
    def update(self, system):
        raise NotImplementedError()
    
    @abstractmethod
    def update_records(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_last_updated(self, time_format) -> str | None:
        raise NotImplementedError()
    
    @abstractmethod
    def validate(self, system) -> bool:
        raise NotImplementedError()
