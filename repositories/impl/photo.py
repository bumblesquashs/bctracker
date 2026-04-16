
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.date import Date
from models.photo import Photo
from models.time import Time

@dataclass(slots=True)
class PhotoRepository:
    
    database: Database
    
    def create(self, path: str, bytes: int, width: int, height: int, context: Context, date: Date | None, time: Time | None, photographer_id: int | None, description: str | None, vehicle_id: str | None, route_number: str | None, stop_number: str | None, approved: bool):
        return self.database.insert(
            table='photo',
            values={
                'path': path,
                'bytes': bytes,
                'width': width,
                'height': height,
                'agency_id': context.agency_id,
                'system_id': context.system_id,
                'date': date.format_db() if date else None,
                'time': time.format_db() if time else None,
                'photographer_id': photographer_id,
                'description': description,
                'vehicle_id': vehicle_id,
                'route_number': route_number,
                'stop_number': stop_number,
                'approved': 1 if approved else 0
            }
        )
    
    def find(self, id: int) -> Photo | None:
        photos = self.database.select(
            table='photo',
            columns={
                'photo.photo_id': 'photo_id',
                'photo.path': 'path',
                'photo.width': 'width',
                'photo.height': 'height',
                'photo.agency_id': 'agency_id',
                'photo.system_id': 'system_id',
                'photo.date': 'date',
                'photo.time': 'time',
                'photographer.photographer_id': 'photographer_id',
                'photographer.name': 'photographer_name',
                'photographer.username': 'photographer_username',
                'photographer.url': 'photographer_url',
                'photo.description': 'description',
                'photo.vehicle_id': 'vehicle_id',
                'photo.route_number': 'route_number',
                'photo.stop_number': 'stop_number',
                'photo.approved': 'approved'
            },
            joins={
                'photographer': {
                    'photographer.photographer_id': 'photo.photographer_id'
                }
            },
            filters={
                'id': id
            },
            limit=1,
            initializer=Photo.from_db
        )
        try:
            return photos[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context = Context(), photographer_id: int | None = None, vehicle_id: str | None = None, route_number: str | None = None, stop_number: str | None = None, approved: bool | None = None, limit: int | None = None) -> list[Photo]:
        return self.database.select(
            table='photo',
            columns={
                'photo.photo_id': 'photo_id',
                'photo.path': 'path',
                'photo.width': 'width',
                'photo.height': 'height',
                'photo.agency_id': 'agency_id',
                'photo.system_id': 'system_id',
                'photo.date': 'date',
                'photo.time': 'time',
                'photographer.photographer_id': 'photographer_id',
                'photographer.name': 'photographer_name',
                'photographer.username': 'photographer_username',
                'photographer.url': 'photographer_url',
                'photo.description': 'description',
                'photo.vehicle_id': 'vehicle_id',
                'photo.route_number': 'route_number',
                'photo.stop_number': 'stop_number',
                'photo.approved': 'approved'
            },
            joins={
                'photographer': {
                    'photographer.photographer_id': 'photo.photographer_id'
                }
            },
            filters={
                'photo.agency_id': context.agency_id,
                'photo.system_id': context.system_id,
                'photographer.photographer_id': photographer_id,
                'photo.vehicle_id': vehicle_id,
                'photo.route_number': route_number,
                'photo.stop_number': stop_number,
                'photo.approved': 1 if approved == True else 0 if approved == False else None
            },
            limit=limit,
            initializer=Photo.from_db
        )
    
    def update(self, id: int, context: Context, date: Date | None, time: Time | None, photographer_id: int | None, description: str | None, vehicle_id: str | None, route_number: str | None, stop_number: str | None, approved: bool):
        self.database.update(
            table='photo',
            values={
                'agency_id': context.agency_id,
                'system_id': context.system_id,
                'date': date.format_db() if date else None,
                'time': time.format_db() if time else None,
                'photographer_id': photographer_id,
                'description': description,
                'vehicle_id': vehicle_id,
                'route_number': route_number,
                'stop_number': stop_number,
                'approved': 1 if approved else 0
            },
            filters={
                'id': id
            }
        )
    
    def delete(self, id: int):
        self.database.delete(
            table='photo',
            filters={
                'id': id
            }
        )
