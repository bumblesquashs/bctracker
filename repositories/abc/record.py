
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from models.bus import Bus
    from models.record import Record

class RecordRepository(ABC):
    
    @abstractmethod
    def create(self, context, bus, date, block, time, trip) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def create_trip(self, record, trip):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, record, time):
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, context, bus, block, trip, limit) -> list[Record]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_trip_ids(self, record) -> list[str]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_recorded_today(self, context, trips) -> dict[str, Bus]:
        raise NotImplementedError()
    
    @abstractmethod
    def find_recorded_today_by_block(self, context) -> dict[str, Bus]:
        raise NotImplementedError()
    
    @abstractmethod
    def count(self, context, bus, block, trip) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_stale_trip_records(self):
        raise NotImplementedError()
