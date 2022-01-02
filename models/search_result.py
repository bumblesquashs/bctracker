
class SearchResult:
    def __init__(self, type, name, description, path, match):
        self.type = type
        self.name = name
        self.description = description
        self.path = path
        self.match = match
    
    def __eq__(self, other):
        return self.match == other.match
    
    def __lt__(self, other):
        if self.match == other.match:
            return self.name < other.name
        return self.match > other.match
    
    def get_json_data(self, system, get_url):
        return {
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'url': get_url(system, self.path)
        }
