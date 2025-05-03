
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.model import Model

class ModelRepository(ABC):
    
    @abstractmethod
    def load(self):
        raise NotImplementedError()
    
    @abstractmethod
    def find(self, model_id) -> Model | None:
        raise NotImplementedError()
