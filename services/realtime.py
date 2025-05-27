
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.timestamp import Timestamp

class RealtimeService(ABC):
    
    @abstractmethod
    def update(self, context):
        raise NotImplementedError()
    
    @abstractmethod
    def update_records(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_last_updated(self, time_format) -> Timestamp | None:
        raise NotImplementedError()
    
    @abstractmethod
    def validate(self, context) -> bool:
        raise NotImplementedError()
