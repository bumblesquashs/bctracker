
from dataclasses import dataclass

from models.context import Context
from models.date import Date
from models.photographer import Photographer
from models.row import Row
from models.time import Time

@dataclass(slots=True)
class Photo:
    
    id: int
    path: str
    bytes: int
    width: int
    height: int
    context: Context
    date: Date | None = None
    time: Time | None = None
    photographer: Photographer | None = None
    description: str | None = None
    vehicle_id: str | None = None
    route_number: str | None = None
    stop_number: str | None = None
    approved: bool = True
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a departure initialized from the given database row'''
        id = row['photo_id']
        path = row['path']
        bytes = row['bytes']
        width = row['width']
        height = row['height']
        context = row.context()
        date = Date.parse(row['date'], context.timezone)
        time = Time.parse(row['time'], context.timezone, True)
        photographer = row.obj('photographer', Photographer.from_db)
        description = row['description']
        vehicle_id = row['vehicle_id']
        route_number = row['route_number']
        stop_number = row['stop_number']
        approved = row['approved'] == 1
        return cls(id, path, bytes, width, height, context, date, time, photographer, description, vehicle_id, route_number, stop_number, approved)
    