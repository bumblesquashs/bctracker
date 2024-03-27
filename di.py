
from typing import Type, TypeVar

D = TypeVar('D')

class Container:
    
    __slots__ = (
        'dependencies'
    )
    
    def __init__(self) -> None:
        self.dependencies = {}
    
    def __getitem__(self, type: Type[D]) -> D:
        return self.dependencies[type]
    
    def __setitem__(self, type, dependency):
        self.dependencies[type] = dependency
    
    def add(self, dependency):
        self.dependencies[type(dependency)] = dependency

di = Container()
