
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.departure import Departure
    from models.route import Route

from dataclasses import dataclass, field

from models.context import Context
from models.departure import Departure
from models.direction import Direction
from models.row import Row
from models.sheet import Sheet
from models.time import Time

import repositories

@dataclass(slots=True)
class Trip:
    '''A list of departures for a specific route and a specific service'''
    
    context: Context
    id: str
    route_id: str
    service_id: str
    block_id: str
    direction_id: int
    shape_id: str
    headsign: str
    
    short_id: str = field(init=False)
    sheets: list[Sheet] = field(init=False)
    
    _departures: list[Departure] | None = field(default=None, init=False)
    _route: Route | None = field(default=None, init=False)
    _direction: Direction | None = field(default=None, init=False)
    _custom_headsigns: list[str] | None = field(default=None, init=False)
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a trip initialized from the given database row'''
        context = row.context()
        trip_id = row['id']
        route_id = row['route_id']
        service_id = row['service_id']
        block_id = row['block_id']
        direction_id = row['direction_id']
        shape_id = row['shape_id']
        headsign = row['headsign']
        return cls(context, trip_id, route_id, service_id, block_id, direction_id, shape_id, headsign)
    
    @property
    def url_id(self):
        '''The ID to use when making trip URLs'''
        return self.id
    
    @property
    def display_id(self):
        '''Formats the trip ID for web display'''
        return self.id.replace(':', ':<wbr />')
    
    @property
    def route(self):
        '''Returns the route associated with this trip'''
        if self._route is None:
            self._route = repositories.route.find(self.context, route_id=self.route_id)
        return self._route
    
    @property
    def service(self):
        '''Returns the service associated with this trip'''
        return self.context.system.get_service(self.service_id)
    
    @property
    def first_stop(self):
        '''Returns the first stop of this trip'''
        departure = self.first_departure
        if departure:
            return departure.stop
        return None
    
    @property
    def last_stop(self):
        '''Returns the last stop of this trip'''
        departure = self.last_departure
        if departure:
            return departure.stop
        return None
    
    @property
    def start_time(self):
        '''Returns the time of the first departure of this trip'''
        departure = self.first_departure
        if departure:
            return departure.time
        return Time.unknown()
    
    @property
    def end_time(self):
        '''Returns the time of the last departure of this trip'''
        departure = self.last_departure
        if departure:
            return departure.time
        return Time.unknown()
    
    @property
    def duration(self):
        '''Returns the total time of this trip'''
        return self.start_time.format_difference(self.end_time)
    
    @property
    def length(self):
        '''Returns the distance travelled on this trip'''
        departure = self.last_departure
        if departure:
            return departure.distance
        return None
    
    @property
    def departures(self):
        '''Returns the departures for this trip'''
        if self._departures is None:
            self._departures = repositories.departure.find_all(self.context, trip=self)
        return self._departures
    
    @property
    def first_departure(self):
        '''Returns the first departure for this trip'''
        try:
            return self.departures[0]
        except IndexError:
            return None
    
    @property
    def last_departure(self):
        '''Returns the last departure for this trip'''
        try:
            return self.departures[-1]
        except IndexError:
            return None
    
    @property
    def direction(self):
        '''Returns the direction for this trip'''
        if self._direction is None:
            departures = self.departures
            if departures:
                self._direction = Direction.calculate(departures[0].stop, departures[-1].stop)
            else:
                self._direction = Direction.UNKNOWN
        return self._direction
    
    @property
    def custom_headsigns(self):
        '''Returns the custom headsigns for this trip'''
        if self._custom_headsigns is None:
            headsigns = [str(d) for d in self.departures if d.headsign]
            previous_headsign = None
            custom_headsigns = []
            for headsign in headsigns:
                if headsign != previous_headsign:
                    custom_headsigns.append(headsign)
                previous_headsign = headsign
            self._custom_headsigns = custom_headsigns
        return self._custom_headsigns
    
    def __post_init__(self):
        id_parts = self.id.split(':')
        if len(id_parts) == 1:
            self.short_id = self.id
        else:
            self.short_id = id_parts[0]
        
        self.sheets = self.context.system.copy_sheets([self.service])
    
    def __str__(self):
        if self.context.prefix_headsigns and self.route:
            return f'{self.route.number} {self.headsign}'
        return self.headsign
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        if self.start_time == other.start_time:
            return self.service < other.service
        return self.start_time < other.start_time
    
    def get_json(self):
        '''Returns a representation of this trip in JSON-compatible format'''
        json = {
            'shape_id': self.shape_id,
            'points': [p.get_json() for p in self.find_points()]
        }
        if self.route:
            json['colour'] = self.route.colour
            json['text_colour'] = self.route.text_colour
        else:
            json['colour'] = '666666'
            json['text_colour'] = '000000'
        return json
    
    def find_points(self):
        '''Returns all points associated with this trip'''
        return repositories.point.find_all(self.context, self.shape_id)
    
    def is_related(self, other):
        '''Checks if this trip has the same route, direction, start time, and end time as another trip'''
        if self.id == other.id:
            return False
        if self.route_id != other.route_id:
            return False
        if self.start_time != other.start_time:
            return False
        if self.end_time != other.end_time:
            return False
        if self.direction_id != other.direction_id:
            return False
        return True
