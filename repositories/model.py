
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.model import Model

class ModelRepository:
    def load(self): pass
    def find(self, model_id) -> Model | None: pass
