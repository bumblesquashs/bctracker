
from abc import ABC, abstractmethod

class CronService(ABC):
    
    @abstractmethod
    def start(self):
        raise NotImplementedError()
    
    @abstractmethod
    def stop(self):
        raise NotImplementedError()
    
    @abstractmethod
    def handle_gtfs(self):
        raise NotImplementedError()
    
    @abstractmethod
    def handle_realtime(self):
        raise NotImplementedError()
