
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.bus import Bus
    from models.record import Record

class RecordRepository(ABC):
    
    @abstractmethod
    def create(self, bus, date, system, block, time, trip) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def create_trip(self, record, trip):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, record, time):
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, system, bus, block, trip, limit) -> list[Record]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_trip_ids(self, record) -> list[str]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_recorded_today(self, system, trips) -> dict[str, Bus]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_stale_trip_records(self):
        raise NotImplementedError()
