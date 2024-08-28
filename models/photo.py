
class Photo:
    
    __slots__ = (
        'id',
        'credit',
        'url',
        'description'
    )
    
    def __init__(self, id, credit, url, description):
        self.id = id
        self.credit = credit
        self.url = url
        self.description = description
    
    def __str__(self):
        return self.description
