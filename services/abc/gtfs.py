
from abc import ABC, abstractmethod

class GTFSService(ABC):
    
    @abstractmethod
    def load(self, context, force_download, update_db):
        raise NotImplementedError()
    
    @abstractmethod
    def validate(self, context) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def update_cache(self, context):
        raise NotImplementedError()
