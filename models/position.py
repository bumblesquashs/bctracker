
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass, field

from models.adherence import Adherence
from models.bus import Bus
from models.occupancy import Occupancy
from models.row import Row
from models.timestamp import Timestamp

import repositories

@dataclass(slots=True)
class Position:
    '''Current information about a bus' coordinates, trip, and stop'''
    
    system: System
    bus: Bus
    trip_id: str | None = None
    stop_id: str | None = None
    block_id: str | None = None
    route_id: str | None = None
    sequence: int | None = None
    lat: float | None = None
    lon: float | None = None
    bearing: float | None = None
    speed: float | None = None
    adherence: Adherence | None = None
    occupancy: Occupancy = field(default=Occupancy.NO_DATA_AVAILABLE)
    timestamp: Timestamp = field(default_factory=Timestamp.now)
    outdated: bool = False
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a position initialized from the given database row'''
        context = row.context()
        bus = context.find_bus(row['vehicle_id'])
        trip_id = row['trip_id']
        stop_id = row['stop_id']
        block_id = row['block_id']
        route_id = row['route_id']
        sequence = row['sequence']
        lat = row['lat']
        lon = row['lon']
        bearing = row['bearing']
        speed = row['speed']
        adherence_value = row['adherence']
        layover = row['layover'] == 1
        if adherence_value is None:
            adherence = None
        else:
            adherence = Adherence(adherence_value, layover)
        occupancy = Occupancy.from_db(row['occupancy'])
        timestamp = Timestamp.parse(row['timestamp'], context.timezone)
        return cls(context.system, bus, trip_id, stop_id, block_id, route_id, sequence, lat, lon, bearing, speed, adherence, occupancy, timestamp)
    
    @property
    def context(self):
        '''The context for this position'''
        return self.system.context
    
    @property
    def has_location(self):
        '''Checks if this position has non-null coordinates'''
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        '''Returns the trip associated with this position'''
        if self.trip_id:
            return self.system.get_trip(self.trip_id)
        return None
    
    @property
    def stop(self):
        '''Returns the stop associated with this position'''
        if self.stop_id:
            return self.system.get_stop(stop_id=self.stop_id)
        return None
    
    @property
    def block(self):
        '''Returns the block associated with this position'''
        if self.block_id:
            return self.system.get_block(self.block_id)
        return None
    
    @property
    def route(self):
        '''Returns the route associated with this position'''
        if self.route_id:
            return self.system.get_route(route_id=self.route_id)
        return None
    
    @property
    def colour(self):
        '''Returns the route colour associated with this position'''
        route = self.route
        if route:
            return route.colour
        return self.context.nis_colour
    
    @property
    def text_colour(self):
        '''Returns the route text colour associated with this position'''
        route = self.route
        if route:
            return route.text_colour
        return self.context.nis_text_colour
    
    @property
    def departure(self):
        '''Returns the departure associated with this position'''
        return repositories.departure.find(self.context, self.trip_id, self.sequence)
    
    def __eq__(self, other):
        return self.bus == other.bus
    
    def __lt__(self, other):
        return self.bus < other.bus
    
    def get_json(self):
        '''Returns a representation of this position in JSON-compatible format'''
        data = {
            'vehicle_id': self.bus.id,
            'bus_display': str(self.bus),
            'bus_url_id': str(self.bus.url_id),
            'system': str(self.system),
            'agency_id': self.context.agency_id,
            'lon': self.lon,
            'lat': self.lat,
            'colour': self.colour,
            'text_colour': self.text_colour,
            'occupancy_name': self.occupancy.value,
            'occupancy_status_class': self.occupancy.status_class,
            'occupancy_icon': self.occupancy.icon,
            'outdated': self.outdated
        }
        year_model = self.bus.year_model
        if year_model:
            data['bus_year_model'] = year_model.replace("'", '&apos;')
        else:
            data['bus_year_model'] = 'Unknown Year/Model'
        model = self.bus.model
        if model and model.type:
            data['bus_icon'] = f'model/type/bus-{model.type.name}'
        else:
            data['bus_icon'] = 'ghost'
        decoration = self.bus.find_decoration()
        if decoration and decoration.enabled:
            data['decoration'] = str(decoration)
        if self.bus.livery:
            data['livery'] = self.bus.livery
        trip = self.trip
        if trip:
            departure = self.departure
            if departure and departure.headsign:
                data['headsign'] = str(departure).replace("'", '&apos;')
            else:
                data['headsign'] = str(trip).replace("'", '&apos;')
            data['route_number'] = trip.route.number
            data['system_id'] = trip.context.system_id
            data['shape_id'] = trip.shape_id
        else:
            data['headsign'] = 'Not In Service'
            data['route_number'] = 'NIS'
        bearing = self.bearing
        if bearing is not None:
            data['bearing'] = bearing
        speed = self.speed
        if speed is not None:
            data['speed'] = speed
        adherence = self.adherence
        if adherence:
            data['adherence'] = adherence.get_json()
        timestamp = self.timestamp
        if timestamp:
            data['timestamp'] = timestamp.value
        return data
