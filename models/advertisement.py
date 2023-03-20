
class Advertisement:
    '''An april fools joke'''
    
    __slots__ = ('id', 'file_name')
    
    @classmethod
    def from_csv(cls, row):
        '''Returns an advertisement initialized from the given CSV row'''
        id = row['id']
        file_name = row['file_name']
        return cls(id, file_name)
    
    def __init__(self, id, file_name):
        self.id = id
        self.file_name = file_name
