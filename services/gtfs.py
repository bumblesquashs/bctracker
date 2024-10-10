
from abc import ABC, abstractmethod

class GTFSService(ABC):
    
    @abstractmethod
    def load(self, system, force_download, update_db):
        raise NotImplementedError()
    
    @abstractmethod
    def validate(self, system) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def update_cache_in_background(self, system):
        raise NotImplementedError()
