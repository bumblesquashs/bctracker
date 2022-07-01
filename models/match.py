
class Match:
    '''A search result with a value indicating how closely it matches the query'''
    
    __slots__ = ('type', 'name', 'description', 'path', 'value')
    
    @classmethod
    def bus(cls, bus_number, order, value):
        return cls('bus', bus_number, str(order), f'bus/{bus_number}', value)
    
    @classmethod
    def route(cls, route, value):
        return cls('route', route.number, route.name, f'routes/{route.number}', value)
    
    @classmethod
    def stop(cls, stop, value):
        return cls('stop', stop.number, stop.name, f'stops/{stop.number}', value)
    
    def __init__(self, type, name, description, path, value):
        self.type = type
        self.name = name
        self.description = description
        self.path = path
        self.value = value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        if self.value == other.value:
            return self.name < other.name
        return self.value > other.value
    
    def get_json(self, system, get_url):
        return {
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'url': get_url(system, self.path)
        }
