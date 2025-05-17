
from abc import ABC, abstractmethod

class BackupService(ABC):
    
    @abstractmethod
    def run(self, date, include_db, delete_files):
        raise NotImplementedError()
