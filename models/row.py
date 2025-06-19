
from dataclasses import dataclass
from typing import Callable, Self, TypeVar

from models.context import Context

T = TypeVar('T')

@dataclass(slots=True)
class Row:
    
    values: dict[str, str | int | float]
    prefix: str | None = None
    
    def make_key(self, key) -> str:
        if self.prefix:
            return f'{self.prefix}_{key}'
        return key
    
    def __getitem__(self, key: str) -> str | int | float | None:
        return self.values[self.make_key(key)]
    
    def get(self, key: str) -> str | int | float | None:
        return self.values.get(self.make_key(key))
    
    def obj(self, key: str, init: Callable[[Self], T]) -> T | None:
        try:
            return init(Row(self.values, self.make_key(key)))
        except:
            return None
    
    def context(self, key: str = 'system_id') -> Context | None:
        return Context.find(system_id=self.get(key))
