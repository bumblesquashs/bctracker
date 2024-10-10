
class Backoff:
    
    __slots__ = (
        'value',
        'target',
        'scale',
        'initial_target'
    )
    
    def __init__(self, scale=2, initial_target=1):
        self.value = 0
        self.target = 1
        self.scale = scale
        self.initial_target = initial_target
    
    def check(self):
        '''Checks if the value has reached the target'''
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
