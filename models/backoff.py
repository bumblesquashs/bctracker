
from dataclasses import dataclass

@dataclass(slots=True)
class Backoff:
    
    value: int = 0
    target: int = 1
    scale: int = 2
    initial_target: int = 1
    max_target: int | None = None
    
    def check(self):
        '''Checks if the value has reached the target'''
        if self.max_target:
            return self.value >= self.target and self.value <= self.max_target
        return self.value >= self.target
    
    def reset(self):
        '''Resets the value and target'''
        self.value = 0
        self.target = self.initial_target
    
    def increase_value(self):
        '''Increases the value without changing the target'''
        self.value += 1
    
    def increase_target(self):
        '''Increases the target and resets the value'''
        self.value = 0
        self.target *= self.scale
