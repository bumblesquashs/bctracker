
from dataclasses import dataclass

from models.row import Row

@dataclass(slots=True)
class Photographer:
    
    id: int
    name: str
    username: str | None = None
    url: str | None = None
    
    @classmethod
    def from_db(cls, row: Row):
        id = row['id']
        name = row['name']
        username = row['username']
        url = row['url']
        return cls(id, name, username, url)
