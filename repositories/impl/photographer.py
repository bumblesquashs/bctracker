
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.photographer import Photographer

@dataclass(slots=True)
class PhotographerRepository:
    
    database: Database
    
    def create(self, name: str, username: str | None, url: str | None):
        return self.database.insert(
            table='photographer',
            values={
                'name': name,
                'username': username,
                'url': url
            }
        )
    
    def find(self, id: int) -> Photographer | None:
        photographers = self.database.select(
            table='photographer',
            columns={
                'photographer_id': 'id',
                'name': 'name',
                'username': 'username',
                'url': 'url'
            },
            filters={
                'id': id
            },
            limit=1,
            initializer=Photographer.from_db
        )
        try:
            return photographers[0]
        except IndexError:
            return None
    
    def find_all(self, limit: int | None = None) -> list[Photographer]:
        return self.database.select(
            table='photographer',
            columns={
                'photographer_id': 'id',
                'name': 'name',
                'username': 'username',
                'url': 'url'
            },
            limit=limit,
            initializer=Photographer.from_db
        )
    
    def update(self, id: int, name: str, username: str | None, url: str | None):
        self.database.update(
            table='photographer',
            values={
                'name': name,
                'username': username,
                'url': url
            },
            filters={
                'id': id
            }
        )
    
    def delete(self, id: int):
        self.database.delete(
            table='photographer',
            filters={
                'id': id
            }
        )
