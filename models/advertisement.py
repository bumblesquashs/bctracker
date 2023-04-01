
class Advertisement:
    '''An april fools joke'''
    
    __slots__ = ('id', 'file_name', 'url')
    
    @classmethod
    def from_csv(cls, row):
        '''Returns an advertisement initialized from the given CSV row'''
        id = row['id']
        file_name = row['file_name']
        url = row['url']
        return cls(id, file_name, url)
    
    def __init__(self, id, file_name, url):
        self.id = id
        self.file_name = file_name
        self.url = url
