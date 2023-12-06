
class DateRange:
    '''A set of dates between starting and ending points'''
    
    __slots__ = ('start', 'end')
    
    @classmethod
    def combine(cls, date_ranges):
        '''Returns a date range that includes all the given date ranges'''
        start = min({r.start for r in date_ranges})
        end = max({r.end for r in date_ranges})
        return cls(start, end)
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __str__(self):
        if self.start == self.end:
            return str(self.start)
        return f'{self.start} to {self.end}'
    
    def __hash__(self):
        return hash((self.start, self.end))
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
    
    def __lt__(self, other):
        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start
    
    def __len__(self):
        return abs((self.end.datetime - self.start.datetime).days) + 1
    
    def __contains__(self, date):
        return self.start <= date <= self.end
    
    def __iter__(self):
        date = self.start
        while date <= self.end:
            yield date
            date = date.next()
    
    def overlaps(self, other):
        '''Checks if this date range overlaps with the given date range'''
        return self.start <= other.end and other.start <= self.end
