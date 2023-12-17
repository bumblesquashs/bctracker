
class Event:
    '''Something that occurred on a specific date'''
    
    __slots__ = (
        'date',
        'name',
        'description'
    )
    
    @property
    def is_today(self):
        return self.date.is_today
    
    def __init__(self, date, name, description=None):
        self.date = date
        self.name = name
        self.description = description
